from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.db.models import Q

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Team
from users.models import Profile
from django.contrib.auth.models import User
from projects.models import Project

from role_permissions.rules import TeamLeaderRequiredMixin


class TeamCreateView(LoginRequiredMixin, TeamLeaderRequiredMixin, CreateView):
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
            self.request.user.profile.save()
            # Redirect
            return super().get_success_url()
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
        # ctx['projects'] = Project.objects.filter(team=team).order_by('-created_at')
        # ctx['active_projects'] = [project for project in ctx['projects'] if project.status is Project.Status.CURRENT]
        # ctx['finished_projects'] = [project for project in ctx['projects'] if project.status is Project.Status.DONE]
        ctx['team_users'] = User.objects.filter(profile__team=team)
        ctx['team_leaders'] = User.objects.filter(profile__team=team, profile__role__name='Team Leader').count()
        ctx['active_projects'] = Project.objects.filter(team=team, status=Project.Status.CURRENT)
        ctx['finished_projects'] = Project.objects.filter(team=team, status=Project.Status.DONE)
        ctx['no_projects_msg'] = 'Dit hold har endnu ikke modtaget nogen projekter.'
        return ctx


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
        print(projects)
        return projects


# THIS VIEW IS NOT IN USE. THE REASON BEING THE VIEW ONLY DISPLAYS DATA WHICH IS ALSO AVAILABLE IN THE TeamDetailView VIEW
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

