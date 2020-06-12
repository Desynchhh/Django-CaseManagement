from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin

def handler(user):
    if user.is_authenticated:
        return redirect('confirm-login')
    return redirect('login')

class TeamLeaderRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.profile.role.name == 'Team Leader'
    
    def handle_no_permission(self):
        return handler(self.request.user)


class ClientRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.profile.role.name == 'Client'
    
    def handle_no_permission(self):
        return handler(self.request.user)
            

class TLOrClientRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        role_name = self.request.user.profile.role.name
        return role_name == 'Team Leader' or role_name == 'Client'
    
    def handle_no_permission(self):
        return handler(self.request.user)


class ProjectOwnerOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.owner

    def handle_no_permission(self):
        return handler(self.request.user)


class NoteOwnerAndTeamLeaderOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        note = self.get_object()
        return self.request.user == note.user or self.request.user.profile.role.name == 'Team Leader'

    def handle_no_permission(self):
        return handler(self.request.user)


class MediumOwnerAndTeamLeaderOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        medium = self.get_object()
        return self.request.user == medium.user or self.request.user.profile.role.name == 'Team Leader'

    def handle_no_permission(self):
        return handler(self.request.user)


class TeamNewUserRequiredMixin(UserPassesTestMixin):
    """Used for pages only accessible to users without a Team"""
    def test_func(self):
        return self.request.user.profile.role.name == 'Team'

    def handle_no_permission(self):
        return handler(self.request.user)


class TeamLeaderOrTeamNewUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        role = self.request.user.profile.role
        return role.name == 'Team' or role.name == 'Team Leader'

    def handle_no_permission(self):
        return handler(self.request.user)


class TeamUserAnyRequiredMixin(UserPassesTestMixin):
    """Used for pages only accessible to users with either role of Team Member or Team Leader"""
    def test_func(self):
        role = self.request.user.profile.role
        return role.name == 'Team Member' or role.name == 'Team Leader'

    def handle_no_permission(self):
        return handler(self.request.user)
