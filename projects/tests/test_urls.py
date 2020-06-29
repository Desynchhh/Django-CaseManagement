from django.test import SimpleTestCase
from django.urls import reverse, resolve
from projects.views import (
    ClientProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    UpdateStatusView,
    TeamAcceptProjectView,
    TeamUserSignUpView,
    NoteCreateView,
    NoteDeleteView,
    ImageCreateView,
    ImageDeleteView
)


# Use SimpleTestCase when NOT interacting with the database
class TestUrls(SimpleTestCase):

    
    def test_create_url_is_resolved(self):
        url = reverse('project-create')
        self.assertEquals(resolve(url).func.view_class, ProjectCreateView)
    

    def test_update_url_is_resolved(self):
        url = reverse('project-update', args=[1, 'project-slug'])
        self.assertEquals(resolve(url).func.view_class, ProjectUpdateView)
    

    def test_client_project_url_is_resolved(self):
        url = reverse('client-projects')
        self.assertEquals(resolve(url).func.view_class, ClientProjectListView)
    

    def test_project_detail_url_is_resolved(self):
        url = reverse('project-detail', args=[1, 'project-slug'])
        self.assertEquals(resolve(url).func.view_class, ProjectDetailView)
    

    def test_project_status_update_url_is_resolved(self):
        url = reverse('project-status-update', args=[1, 'project-slug'])
        self.assertEquals(resolve(url).func.view_class, UpdateStatusView)
    

    def test_project_accept_url_is_resolved(self):
        url = reverse('project-accept', args=[1, 'project-slug'])
        self.assertEquals(resolve(url).func.view_class, TeamAcceptProjectView)
    

    def test_project_sign_up_url_is_resolved(self):
        url = reverse('project-sign-up', args=[1, 'project-slug'])
        self.assertEquals(resolve(url).func.view_class, TeamUserSignUpView)
    

    def test_note_create_url_is_resolved(self):
        url = reverse('note-create', args=[1, 'project-slug'])
        self.assertEquals(resolve(url).func.view_class, NoteCreateView)
    

    def test_note_delete_url_is_resolved(self):
        url = reverse('note-delete', args=[1, 'project-slug', 1])
        self.assertEquals(resolve(url).func.view_class, NoteDeleteView)
    

    def test_image_create_url_is_resolved(self):
        url = reverse('image-create', args=[1, 'project-slug'])
        self.assertEquals(resolve(url).func.view_class, ImageCreateView)
    

    def test_image_delete_url_is_resolved(self):
        url = reverse('image-delete', args=[1, 'project-slug', 1])
        self.assertEquals(resolve(url).func.view_class, ImageDeleteView)