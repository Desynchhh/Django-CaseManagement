from django.shortcuts import (
    render,
    redirect,
    reverse,
    get_object_or_404
)

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

from .models import Project
from .forms import UpdateProjectStatusForm

from role_permissions.rules import (
    TeamLeaderRequiredMixin,
    TLOrClientRequiredMixin,
    ClientRequiredMixin
)

# Create your views here.
class TeamProjectListView(LoginRequiredMixin, TeamLeaderRequiredMixin, ListView):
    model = Project
    template_name = 'projects/team_project_list.html'

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

        for project in projects:
            if project.status == Project.Status.CURRENT:
                ctx['active_projects'].append(project)
            if project.status == Project.Status.DONE:
                ctx['finished_projects'].append(project)
        return ctx


class ClientProjectListView(LoginRequiredMixin, ClientRequiredMixin, ListView):
    model = Project


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['project'] = get_object_or_404(Project, pk=self.kwargs['pk'])
        ctx['project_is_done'] = ctx['project'] == Project.Status.DONE
        ctx['form'] = UpdateProjectStatusForm(instance=ctx['project'])
        return ctx

class ProjectCreateView(LoginRequiredMixin, TLOrClientRequiredMixin, SuccessMessageMixin, CreateView):
    model = Project
    fields = ['name', 'description', 'team']
    success_message = 'Projektet er blevet oprettet!'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['legend'] = 'Opret nyt projekt'
        ctx['btn'] = 'Opret'
        return ctx


class ProjectUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Project
    fields = ['name', 'description']
    success_message = 'Projektet er blevet opdateret.'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['legend'] = 'Opdater projekt'
        ctx['btn'] = 'Gem'
        return ctx


class UpdateStatusView(LoginRequiredMixin, TeamLeaderRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        return reverse('project-detail', kwargs=kwargs)

    def post(self, request, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        form = UpdateProjectStatusForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Projektets status er blevet opdateret!')
        else:
            messages.danger(request, 'Noget gik galt. Projektets status er derfor <b>ikke</b> blevet opdateret.')
        return redirect(reverse('project-detail', kwargs=kwargs))
