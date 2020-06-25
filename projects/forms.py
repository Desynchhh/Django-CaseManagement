from django import forms

from .models import Project, Media

class UpdateProjectStatusForm(forms.ModelForm):
    status = forms.ChoiceField(choices=Project.Status.choices)

    class Meta:
        model = Project
        fields = ('status',)


# VIEWS WITH THIS FORM IS NO LONGER IN USE
# class EditUsersMultipleChoiceField(forms.ModelChoiceField):
#     def label_from_instance(self, obj):
#         return obj.user.get_full_name()

# class EditUsersForm(forms.ModelForm):
#     users = EditUsersMultipleChoiceField(
#         queryset=None,
#         label='Brugere'
#     )

#     class Meta:
#         model = Project
#         fields = ('users',)
