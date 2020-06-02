from django.shortcuts import render, get_object_or_404

from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Team
from users.models import Profile
from django.contrib.auth.models import User
from projects.models import Project

# Create your views here.
# def index(request):
#     team_users = Profile.objects.filter(team=request.user.profile.team)
#     return render(request, 'teams/index.html', {"users":team_users})
class TeamLeaderRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.profile.role.name == 'Team Leader'


class TeamListView(LoginRequiredMixin, TeamLeaderRequiredMixin, ListView):
    model = Profile
    template_name = 'teams/index.html'

    def get_queryset(self):
        return Profile.objects.filter(team=self.request.user.profile.team)


class TeamDetailView(LoginRequiredMixin, TeamLeaderRequiredMixin, DetailView):
    model = Team

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = get_object_or_404(Team, pk=self.kwargs['pk'], slug=self.kwargs['slug'])
        context['team'] = team
        context['projects'] = Project.objects.filter(team=team).order_by('-created_at')
        context['active_projects'] = [project for project in context['projects'] if project.status is Project.Status.CURRENT]
        context['finished_projects'] = [project for project in context['projects'] if project.status is Project.Status.DONE]
        context['team_users'] = User.objects.filter(profile__team=team)
        context['team_leaders'] = User.objects.filter(profile__team=team, profile__role__name='Team Leader').count()
        return context
