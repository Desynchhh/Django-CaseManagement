from django.test import SimpleTestCase
from projects.forms import UpdateProjectStatusForm
from projects.models import Project


class TestForms(SimpleTestCase):

    def test_update_project_status_form_valid_data(self):
        form = UpdateProjectStatusForm(data={
            'status': Project.Status.DONE
        })

        self.assertTrue(form.is_valid())


    def test_update_project_status_form_no_data(self):
        form = UpdateProjectStatusForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
