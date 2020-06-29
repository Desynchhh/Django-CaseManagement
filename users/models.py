from django.db import models

from django.contrib.auth.models import User
from teams.models import Team

from django.core.validators import RegexValidator
from django.utils import timezone

from PIL import Image

# Create your models here.
class Role(models.Model):
    name = models.CharField(
        max_length = 255,
        unique=True,
        help_text="Et beskrivende navn til rollen.",
        error_messages={"required": "Navnefeltet er påkrævet."}
    )
    display_name = models.CharField(
        max_length = 255,
        help_text="Navnet der bliver vist på siden.",
        error_messages={"required": "Visningsnavnefeltet er påkrævet."}
    )
    description = models.CharField(
        max_length = 255,
        help_text="En lille beskrivelse af rollen.",
        error_messages={"required": "Beskrivelsesfeltet er påkrævet."}
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name
        

numbers_only = RegexValidator(r'[0-9]*', "Dit telefonnummer kan kun indeholde tal.")
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_DEFAULT,
        blank=True,
        null=True,
        default=None,
        help_text='Arbejdsholdet brugeren skal tilkobles.',
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
        help_text="Brugerens rolle. Denne vil bestemme hvilke rettigheder De har i app'en, samt hvilke sider De kan tilgå."
    )

    phone_number = models.CharField(
        max_length = 8,
        validators=[numbers_only],
        help_text='Et telefonnummer du kan kontaktes på.',
        blank=True,
        null=True,
        default=None
    )
    pfp = models.ImageField(
        upload_to='img/pfp/',
        default='img/default.jpg'
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Resize image after upload
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.pfp.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.pfp.path)

    def __str__(self):
        return f"{self.user.username}'s Profile"
