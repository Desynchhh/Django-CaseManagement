from django.test import TestCase, RequestFactory
from django.urls import reverse

from django.contrib.auth.models import User
from projects.models import Project, Note, Media
from teams.models import Team
from users.models import Role

from projects.views import ClientProjectListView

import json

class TestViews(TestCase):

    # setUp is ran before any test is (sort of like __init__)
    def setUp(self):
        self.factory = RequestFactory()

        # URLS
        self.client_projects_url = reverse('client-projects')

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
            name='project1',
            description='project1 desc'
        )


    def test_client_project_list_GET_not_authenticated(self):
        response = self.client.get(self.client_projects_url)
        
        self.assertEquals(response.status_code, 302)


    def test_client_project_list_GET_authenticated(self):
        # Create a hand-crafted Request object
        request = self.factory.get(self.client_projects_url)
        # Add user to Request object
        request.user = self.client_user
        response = ClientProjectListView.as_view()(request)

        self.assertEquals(response.status_code, 200)
        # self.assertTemplateUsed(response, 'projects/client_project_list.html')
