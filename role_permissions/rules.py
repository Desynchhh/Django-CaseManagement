from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin

from projects.models import Project

# Override once then inherit this class, instead of overriding for every rule.
class UserPassesTestHandler(UserPassesTestMixin):
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('confirm-login')
        return redirect('login')


class TeamLeaderRequiredMixin(UserPassesTestHandler):
    def test_func(self):
        return self.request.user.profile.role.name == 'Team Leader'


class TeamMemberRequiredMixin(UserPassesTestHandler):
    def test_func(self):
        return self.request.user.profile.role.name == 'Team Member'


class ClientRequiredMixin(UserPassesTestHandler):
    def test_func(self):
        return self.request.user.profile.role.name == 'Client'
            

class TLOrClientRequiredMixin(UserPassesTestHandler):
    def test_func(self):
        role_name = self.request.user.profile.role.name
        return role_name == 'Team Leader' or role_name == 'Client'


class ProjectOwnerOnlyMixin(UserPassesTestHandler):
    def test_func(self):
        project = self.get_object()
        return self.request.user == project.owner


class TeamNewUserRequiredMixin(UserPassesTestHandler):
    """Used for pages only accessible to users without a Team"""
    def test_func(self):
        return self.request.user.profile.role.name == 'Team'


class TeamLeaderOrTeamNewUserRequiredMixin(UserPassesTestHandler):
    def test_func(self):
        role = self.request.user.profile.role
        return role.name == 'Team' or role.name == 'Team Leader'


class TeamUserAnyRequiredMixin(UserPassesTestHandler):
    """Used for pages only accessible to users with either role of Team Member or Team Leader"""
    def test_func(self):
        role = self.request.user.profile.role
        return role.name == 'Team Member' or role.name == 'Team Leader'


class ProjectUsersOnly(UserPassesTestHandler):
    def test_func(self):
        print(self.kwargs)
        project = Project.objects.get(pk=self.kwargs['pid'], slug=self.kwargs['slug'])
        user = self.request.user

        if user == project.owner or user == project.leader:
            return True
        elif self.request.user.profile in project.users.all():
            return True
        return False
