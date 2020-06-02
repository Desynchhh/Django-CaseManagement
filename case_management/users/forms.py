from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

letters_only = RegexValidator(r'[a-zA-Z ]+', 'Dit navn kan kun bestå af bogstaver.')
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        validators=[letters_only],
        label='Fornavn',
        error_messages={"required": "Fornavnsfeltet er påkrævet."}
    )
    last_name = forms.CharField(
        required=True,
        validators=[letters_only],
        label='Efternavn',
        error_messages={"required": "Efternavnsfeltet er påkrævet."}
    )
    email = forms.EmailField(
        required=True,
        label='Email',
        error_messages={"required": "Emailfeltet er påkrævet."}
    )
    error_messages = {
        'password_mismatch': 'De 2 kodeordsfelter matchede ikke.',
    }
    password1 = forms.CharField(
        label="Kodeord",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Bekræft kodeord",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="Indtast samme kodeord som ovenfor.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = "Kun bogstaver, tal og @/./+/-/_"

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
