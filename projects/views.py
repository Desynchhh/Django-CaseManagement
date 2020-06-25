from django.shortcuts import (
    render,
    redirect,
    reverse,
    get_object_or_404
)
from django.http import Http404

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

# from users.models import Profile
from .models import Project, Note, Media
from .forms import UpdateProjectStatusForm #, EditUsersForm

from role_permissions.rules import (
    TeamLeaderRequiredMixin,
    TeamMemberRequiredMixin,
    TLOrClientRequiredMixin,
    ClientRequiredMixin,
    ProjectOwnerOnlyMixin,
    ProjectUsersOnly
)

from blobstorage import AzureStorage

# Create your views here.
class ClientProjectListView(LoginRequiredMixin, ClientRequiredMixin, ListView):
    """
    This view lists a table of all projects a user has created.
    A Client can only see their own projects.
    Only logged in users with a role of "Client" can access this view.
    """
    model = Project
    template_name = 'projects/client_project_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['no_projects_msg'] = 'Du har ikke oprettet nogen projekter endnu.'
        return ctx

    def get_queryset(self):
        """Only get projects where the logged in user is the owner"""
        return self.model.objects.filter(owner=self.request.user)


class ProjectDetailView(LoginRequiredMixin, DetailView):
    """
    Renders a template with detailed information about the specified project.
    All logged in users have access to this view.
    """
    model = Project

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['project'] = get_object_or_404(Project, pk=self.kwargs['pk'])
        ctx['project_is_done'] = ctx['project'] == Project.Status.DONE
        ctx['form'] = UpdateProjectStatusForm(instance=ctx['project'])
        return ctx


class ProjectCreateView(LoginRequiredMixin, TLOrClientRequiredMixin, SuccessMessageMixin, CreateView):
    """
    On GET requests: Renders a template with a form to create a project.
    On POST requests: Validates the submitted form and creates a project entry in the DB. Then redirects to ProjectDetailView.
    Only logged in users with a role of either Team Leader or Client has access to this view.
    """
    model = Project
    fields = ('name', 'description', 'team')
    success_message = 'Projektet er blevet oprettet!'

    def form_valid(self, form):
        # Set model fields that are not displayed on the form
        form.instance.owner = self.request.user

        # Save DB entry
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['legend'] = 'Opret nyt projekt'
        ctx['btn'] = 'Opret'
        return ctx


class ProjectUpdateView(LoginRequiredMixin, ProjectOwnerOnlyMixin, SuccessMessageMixin, UpdateView):
    """
    On GET requests: Renders a template with a form to update certain fields on a project.
    On POST requests: Validates the submitted form and PATCHes its entry in the DB. Then redirects to ProjectDetailView.
    Only the specified project's owner has access to this view.
    """
    model = Project
    fields = ['name', 'description']
    success_message = 'Projektet er blevet opdateret.'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['legend'] = 'Opdater projekt'
        ctx['btn'] = 'Gem'
        ctx['update'] = True
        return ctx


class UpdateStatusView(LoginRequiredMixin, TeamLeaderRequiredMixin, TemplateView):
    """
    Team Leaders use this view to update a project's status between DONE (Færdiggjort) and CURRENT (Igangværende).
    Only logged in users with a role of Team Leader have access to this view.
    This view is only meant to be POSTed to.
    """
    
    # View SHOULD never receive a GET request.
    def get(self, request, **kwargs):
        return reverse('project-detail', kwargs=kwargs)

    def post(self, request, **kwargs):
        # Get project
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        
        # Validate & save form
        form = UpdateProjectStatusForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Projektets status er blevet opdateret!')
        else:
            messages.danger(request, 'Noget gik galt. Projektets status er derfor <b>ikke</b> blevet opdateret.')
        # Redirect
        return redirect(reverse('project-detail', kwargs=kwargs))


class TeamAcceptProjectView(LoginRequiredMixin, TeamLeaderRequiredMixin, TemplateView):
    """
    Team Leaders use this view to claim a project. This means the team has accepted the project and Team Members can sign up to work on them.
    Only logged in users with a role of Team Leader have access to this view.
    This view is only meant to be POSTed to
    """

    # View SHOULD never receive a GET request.
    def get(self, request, **kwargs):
        return redirect(reverse('project-detail', kwargs=kwargs))

    def post(self, request, **kwargs):
        # Get project
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        
        # Get user's data
        user = self.request.user
        team = user.profile.team
        
        # Update project's fields
        project.team = team
        project.leader = user
        project.status = Project.Status.CURRENT
        project.users.add(user.profile)
        project.save()

        # Redirect
        return redirect(reverse('project-detail', kwargs=kwargs))


class TeamUserSignUpView(LoginRequiredMixin, TeamMemberRequiredMixin, TemplateView):
    """
    This view allows Team Members to sign up to work on a project. Team Members can only work on a single project at a time.
    Only logged in users with a role of Team Member have access to this view.
    This view is only meant to be POSTed to.
    """

    # View SHOULD never receive a GET request.
    def get(self, request, **kwargs):
        return redirect(reverse('confirm-login'))

    def post(self, request, **kwargs):
        project = get_object_or_404(Project, pk=kwargs['pk'], slug=kwargs['slug'])
        user = request.user.profile

        # Detach the user from their old project
        if user.project_set.exists():
            old_project = user.project_set.first()
            user.project_set.remove(old_project)
        
        # Attach the user to the current project
        user.project_set.add(project)

        # Redirect
        return redirect(reverse('project-detail', kwargs=kwargs))


class NoteCreateView(LoginRequiredMixin, ProjectUsersOnly, SuccessMessageMixin, CreateView):
    """
    On GET requests: Renders a template with a form to create a new Note on the project in the URL.
    On POST requests: Validates the submitted form and creates a note entry associated with the Project in the DB. Then redirects to ProjectDetailView.
    Only logged in users who are associated with the Project have access to this view (projectusers, leader, owner)
    """
    
    model = Note
    fields = ("title", "description")
    success_message = 'Noten er blevet oprettet på projektet.'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['project'] = Project.objects.get(pk=self.kwargs['pid'], slug=self.kwargs['slug'])
        return ctx

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.project = Project.objects.get(pk=self.kwargs['pid'])
        return super().form_valid(form)


class NoteDeleteView(LoginRequiredMixin, TeamLeaderRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    On GET requests: Renders a template where users confirm whether or not they are certain they want to delete the related note.
    On POST requests: Deletes the note entry from the DB. Then redirects to ProjectDetailView.
    Only logged in users with the role of Team Leader have access to this view.
    """
    
    model = Note
    success_message = 'Noten er blevet slettet fra projektet.'

    def get_success_url(self):
        return reverse('project-detail', kwargs={"pk": self.kwargs['pid'], "slug": self.kwargs['slug']})


class ImageCreateView(LoginRequiredMixin, ProjectUsersOnly, SuccessMessageMixin, CreateView):
    """
    On GET requests: Renders a template with a form to create a new Media (image) on the project in the URL.
    On POST requests: Validates the submitted form and creates an image entry associated with the Project in the DB. Then redirects to ProjectDetailView.
    Only logged in users who are associated with the Project have access to this view (projectusers, leader, owner)
    """
    model = Media
    fields = ('title', 'description')
    # template_name = "projects/media_form.html"
    success_message = 'Billedet er blevet tilføjet til projektet.'
    
    def get_success_url(self):
        return reverse('project-detail', kwargs={"pk": self.kwargs.get('pid'), "slug": self.kwargs.get('slug')})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['project'] = Project.objects.get(pk=self.kwargs.get('pid'), slug=self.kwargs.get('slug'))
        return ctx

    def form_valid(self, form):
        # Get the Project the Image is being uploaded to
        project = Project.objects.get(pk=self.kwargs.get('pid'))
        # Get image from the form
        image = self.request.FILES.get('img')
        
        # Upload to Azure Storage
        azure = AzureStorage()
        blob_url = azure.upload_blob(project.azure_container, image)

        # Set model fields that are not on the form
        form.instance.user = self.request.user
        form.instance.project = project
        form.instance.blob = image.name
        form.instance.blob_url = blob_url

        # return redirect(reverse('image-create', kwargs={"pid": self.kwargs.get('pid'), "slug": self.kwargs.get('slug')}))
        # Create DB entry
        return super().form_valid(form)


class ImageDeleteView(LoginRequiredMixin, TeamLeaderRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    On GET requests: Renders a template where users confirm whether or not they are certain they want to delete the related image.
    On POST requests: Deletes the image entry from the DB. Then redirects to ProjectDetailView.
    Only logged in users with the role of Team Leader have access to this view.
    """

    model = Media
    success_message = 'Billedet er blevet fjernet fra projektet.'

    def get_success_url(self):
        return reverse('project-detail', kwargs={"pk": self.kwargs.get('pid'), "slug": self.kwargs.get('slug')})



# USERS NOW SIGN UP FOR PROJECTS RATHER THAN BEING ASSIGNED TO THEM. THUS THIS VIEW IS NO LONGER IN USE
# class ProjectEditUsersView(LoginRequiredMixin, TeamLeaderRequiredMixin, TemplateView):
#     """This view is used by Team Leaders to attach Team Members to Projects."""
#     template_name = 'projects/project_edit_users.html'

#     def get(self, request, **kwargs):
#         # Get project and its users (except the project leader)
#         project = get_object_or_404(Project, pk=kwargs['pk'])
#         project_users = project.users.all().exclude(user=project.leader)

#         # Get all users in the project's team who are not attached to it
#         team = request.user.profile.team
#         team_users = team.profile_set.all().exclude(pk__in=project_users)

#         # Instantiate form for adding users to the project
#         add_form = EditUsersForm()
#         add_form.fields['users'].queryset = team_users

#         # Instantiate form for removing users from the project
#         remove_form = EditUsersForm()
#         remove_form.fields['users'].queryset = project_users

#         # Template context
#         ctx = {
#             'project': project,
#             'team_users': team_users,
#             'project_users': project_users,
#             'add_form': add_form,
#             'remove_form': remove_form
#         }
#         # Render template
#         return render(request, self.template_name, context=ctx)

#     def post(self, request, **kwargs):
#         # Get the project and the user being added to / removed from it
#         project = get_object_or_404(Project, pk=kwargs['pk'])
#         user = get_object_or_404(Profile, pk=request.POST['users'])

#         # Get all users attached to project
#         project_users = project.users.all()

#         # Check if user should be added or removed. Act accordingly
#         if user in project_users:   # Remove
#             project.users.remove(user)
#         else:                       # Add
#             project.users.add(user)
#         # Redirect
#         return redirect(reverse('project-edit-users', kwargs=kwargs))


# PROJECTS SHOULD NOT BE DELETABLE FROM THE FRONTEND FACING APPLICATION.
# class ProjectDeleteView(LoginRequiredMixin, ProjectOwnerOnlyMixin, SuccessMessageMixin, DeleteView):
#     model = Project
#     success_message = 'Projektet er blevet slettet.'

#     def get_success_url(self):
#         profile = self.request.user.profile
#         if profile.role.name == 'Team Leader':
#             return reverse(
#                 'team-projects',
#                 kwargs={
#                     "pk": profile.team.pk,
#                     "slug": profile.team.slug
#                 }
#             )
#         elif profile.role.name == 'Client':
#             return reverse('client-projects')

#     # CHECK IF THE LOGGED IN USER OWNS THE PROJECT. THIS IS NOW DONE IN ProjectOwnerOnlyMixin INSTEAD
#     # def get_object(self, queryset=None):
#     #     """ Hook to ensure object is owned by request.user. """
#     #     obj = super().get_object()
#     #     if not obj.owner == self.request.user:
#     #         raise Http404
#     #     return obj
