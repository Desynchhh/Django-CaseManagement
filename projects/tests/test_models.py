from django.test import TestCase
from projects.models import Project, Note, Media
from teams.models import Team
from users.models import Role
from django.contrib.auth.models import User

class TestModels(TestCase):

    def setUp(self):
        # Roles
        self.team_leader_role = Role.objects.create(
            name='Team_Leader',
            display_name='Instruktør',
            description='Hold leder'
        )
        self.client_role = Role.objects.create(
            name='Client',
            display_name='Klient',
            description='Client'
        )

        # Teams
        self.team = Team.objects.create(name='Team', description='Team desc')

        # Users
        self.client_user = User.objects.create_user('client')
        self.client_user.profile.role = self.client_role
        self.client_user.profile.save()

        self.team_leader_user = User.objects.create_user('team_leader')
        self.team_leader_user.profile.role = self.team_leader_role
        self.team_leader_user.profile.team = self.team
        self.team_leader_user.profile.save()

        # Project
        self.project = Project.objects.create(
            team=self.team,
            owner=self.client_user,
            leader=self.team_leader_user,
            name='project 1',
            description='project1 desc'
        )

    def test_project_is_assigned_slug_on_creation(self):
        self.assertEquals(self.project.slug, 'project-1')