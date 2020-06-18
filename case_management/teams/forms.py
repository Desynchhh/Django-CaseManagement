from django import forms
from users.models import Profile, Role
from django.db.models import Q


# Custom class inheriting from ModelChoiceField, in order to change the text shown in a Select field's options.
class TeamUserRoleChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.display_name


# Custom form to limit the amount of options in the Select field
class UpdateTeamUserRoleForm(forms.ModelForm):
    role = forms.ModelChoiceField(
        queryset=Role.objects.filter(Q(name='Team Leader') | Q(name='Team Member')),
        label='Roller'
    )
    # roles = TeamUserRoleChoiceField(
    #     queryset=Role.objects.filter(Q(name='Team Leader') | Q(name='Team Member')),
    #     label='Roller'
    # )

    class Meta:
        model = Profile
        fields = ('role',)
