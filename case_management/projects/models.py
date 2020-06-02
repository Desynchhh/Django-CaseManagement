from django.db import models

from django.utils.text import slugify
from django.utils import timezone

# from teams.models import Team
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):
    class Status(models.TextChoices):
        PENDING = ('PENDING', 'Modtaget')
        CURRENT = ('CURRENT', 'Igangværende')
        DONE = ('DONE', 'Færdig')


    team = models.OneToOneField(
        'teams.Team',
        on_delete=models.SET_DEFAULT,
        blank=True,
        null=True,
        default=None
    )

    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='owner'
    )
    leader = models.OneToOneField(
        User,
        on_delete=models.SET_DEFAULT,
        related_name='leader',
        blank=True,
        null=True,
        default=None
    )

    name = models.CharField(
        max_length=255,
        help_text='Navnet på dit projekt.',
        error_messages={"required":"Navnefeltet er påkrævet."}    
    )
    description = models.TextField(
        help_text='En klar og detaljeret beskrivelse af projektet.',
        error_messages={"required":"Beskrivelsesfeltet er påkrævet"}
    )
    slug = models.SlugField(max_length=255, blank=True)

    status = models.CharField(
        max_length = 255,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save()

    def __str__(self):
        return self.name
