from django.contrib.auth.mixins import UserPassesTestMixin

class TeamLeaderRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.profile.role.name == 'Team Leader'

class ClientRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.profile.role.name == 'Client'

class TLOrClientRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        role_name = self.request.user.profile.role.name
        return role_name == 'Team Leader' or role_name == 'Client'