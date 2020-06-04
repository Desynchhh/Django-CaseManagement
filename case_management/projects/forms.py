from django import forms

from .models import Project

class UpdateProjectStatusForm(forms.ModelForm):
    status = forms.ChoiceField(choices=Project.Status.choices)

    class Meta:
        model = Project
        fields = ['status']