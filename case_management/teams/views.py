from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import Http404
from django.contrib import messages

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Team
from .forms import UpdateTeamUserRoleForm
from users.models import Profile, Role
from django.contrib.auth.models import User
from projects.models import Project

from role_permissions.rules import (
    TeamLeaderRequiredMixin,
    TeamNewUserRequiredMixin,
    TeamLeaderOrTeamNewUserRequiredMixin
)


class TeamNewUserView(LoginRequiredMixin, TeamNewUserRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'teams/team_new_user.html')


class TeamCreateView(LoginRequiredMixin, TeamLeaderOrTeamNewUserRequiredMixin, CreateView):
    model = Team
    fields = ['name', 'description']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['legend'] = 'Opret nyt hold'
        ctx['btn'] = 'Opret'
        return ctx
    
    def form_valid(self, form):
        if self.request.user.profile.team is None:
            # Save the form instance
            super().form_valid(form)
            # Set user's team to be the one they just created
            self.request.user.profile.team = form.instance
            self.request.user.profile.role = Role.objects.get(name='Team Leader')
            self.request.user.profile.save()
            # Redirect
            return redirect(reverse('team-detail', kwargs={"pk": form.instance.pk, "slug": form.instance.slug}))
        else:
            return super().form_valid(form)


class TeamUpdateView(LoginRequiredMixin, TeamLeaderRequiredMixin, UpdateView):
    model = Team
    fields = ['name', 'description']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['legend'] = 'Opdater hold'
        ctx['btn'] = 'Gem'
        return ctx
    
    def get_object(self, queryset=None):
        team = super().get_object()
        print(team)
        print(self.request.user.profile.team)
        if team != self.request.user.profile.team:
            raise Http404
        return team


class TeamDetailView(LoginRequiredMixin, TeamLeaderRequiredMixin, DetailView):
    model = Team

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        team = get_object_or_404(Team, pk=self.kwargs['pk'], slug=self.kwargs['slug'])
        
        ctx['team'] = team
        ctx['team_users'] = User.objects.filter(profile__team=team)
        ctx['team_leaders'] = User.objects.filter(profile__team=team, profile__role__name='Team Leader').count()

        ctx['projects'] = Project.objects.filter(team=team).exclude(leader=None)
        ctx['active_projects'] = Project.objects.filter(team=team, status=Project.Status.CURRENT)
        ctx['finished_projects'] = Project.objects.filter(team=team, status=Project.Status.DONE)
        ctx['no_projects_msg'] = 'Dit hold har endnu ikke modtaget nogen projekter.'
        # ctx['projects'] = Project.objects.filter(team=team).order_by('-created_at')
        # ctx['active_projects'] = [project for project in ctx['projects'] if project.status is Project.Status.CURRENT]
        # ctx['finished_projects'] = [project for project in ctx['projects'] if project.status is Project.Status.DONE]
        return ctx


class TeamAddUser(LoginRequiredMixin, TeamLeaderRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        teamless_role = Role.objects.get(name='Team')
        team_users = User.objects.filter(profile__team=None, profile__role=teamless_role)
        ctx = {
            "team_users": team_users
        }
        return render(request, 'teams/team_add_user.html', context=ctx)


    def post(self, request, **kwargs):
        user_pk = request.POST['user_pk']
        user = get_object_or_404(User, pk=user_pk)
        if user.profile.team == None:
            team = Team.objects.get(pk=kwargs.get('pk'), slug=kwargs.get('slug'))
            role = Role.objects.get(name='Team Member')
            user.profile.team = team
            user.profile.role = role
            user.profile.save()
            messages.success(request, f'{user.username} er nu tilføjet til {team.name} som elev!')
        else:
            messages.danger(request, f'{user.username} er allerede på et hold, og kan derfor ikke tilføjes.')
        return redirect(reverse('team-add-user', kwargs=kwargs))


class TeamUserUpdate(LoginRequiredMixin, TeamLeaderRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateTeamUserRoleForm
    template_name = 'teams/team_user_form.html'
    
    def get_object(self, queryset=None):
        return Profile.objects.get(user__pk=self.kwargs.get('pk'))

    def get_success_url(self):
        return reverse('team-detail', kwargs={
            "pk": self.kwargs.get('tpk'),
            "slug": self.kwargs.get('slug')
        })

    # def form_valid(self, form):
    #     print(form.instance.role)
    #     print(dir(form))
    #     return super().form_valid(form)


class TeamProjectListView(LoginRequiredMixin, TeamLeaderRequiredMixin, ListView):
    model = Project
    template_name = 'teams/team_project_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # ctx['active_projects'] = Project.objects.filter(
        #     team__pk=self.kwargs['pk'],
        #     status=Project.Status.CURRENT
        # ).order_by('-created_at')

        # ctx['finished_projects'] = Project.objects.filter(
        #     team__pk=self.kwargs['pk'],
        #     status=Project.Status.DONE
        # ).order_by('-created_at')

        projects = Project.objects.filter(team__pk=self.kwargs['pk'], team__slug=self.kwargs['slug']).order_by('-created_at')
        ctx['active_projects'] = []
        ctx['finished_projects'] = []
        ctx['no_projects_msg'] = 'Der er ingen projekter under denne kategori.'

        for project in projects:
            # Ignore PENDING projects
            if project.status == Project.Status.CURRENT:
                ctx['active_projects'].append(project)
            if project.status == Project.Status.DONE:
                ctx['finished_projects'].append(project)
        return ctx


class TeamProjectRequestListView(LoginRequiredMixin, TeamLeaderRequiredMixin, ListView):
    model = Project
    template_name = 'teams/team_project_request_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['no_projects_msg'] = 'Der er ingen nye projekter at finde.'
        return ctx

    def get_queryset(self):
        projects = Project.objects.filter(team__pk=self.kwargs['pk'], leader=None)
        return projects


# THIS VIEW IS NOT IN USE. THE REASON BEING IT ONLY DISPLAYS DATA WHICH IS ALSO AVAILABLE IN THE TeamDetailView VIEW
# class TeamListView(LoginRequiredMixin, TeamLeaderRequiredMixin, ListView):
#     model = Profile
#     template_name = 'teams/index.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['team'] = get_object_or_404(Team, pk=self.kwargs['pk'], slug=self.kwargs['slug'])
#         context['team_users'] = User.objects.filter(profile__team=context['team'])
#         return context

#     # def get_queryset(self):
#     #     return Profile.objects.filter(team=self.request.user.profile.team)
