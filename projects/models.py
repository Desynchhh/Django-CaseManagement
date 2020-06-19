from django.db import models

from django.shortcuts import reverse
from django.utils.text import slugify
from django.utils import timezone

from django.contrib.auth.models import User

import os

# Create your models here.
class Project(models.Model):

    class Status(models.TextChoices):
        PENDING = ('PENDING', 'Modtaget')
        CURRENT = ('CURRENT', 'Igangværende')
        DONE = ('DONE', 'Færdig')

    team = models.ForeignKey(
        'teams.Team',
        on_delete=models.SET_DEFAULT,
        # blank=True,
        # null=True,
        default=None,
        help_text='Holdet i firmaet, som du ønsker skal tage imod dit projekt.'# <br>Hvis du ikke vælger et, kan ethvert hold tage imod det.'
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=None,
        related_name='owner'
    )
    leader = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        related_name='leader',
        blank=True,
        null=True,
        default=None
    )
    users = models.ManyToManyField("users.profile", blank=True)

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

    def worker_count(self):
        # if self.leader is None:
        #     return self.users.all().count()
        return self.users.all().exclude(user=self.leader).count()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save()

    def get_absolute_url(self):
        return reverse("project-detail", kwargs={"pk": self.pk, "slug": self.slug})
    
    def __str__(self):
        return self.name


class Note(models.Model):
    title = models.CharField(
        max_length=255,
        error_messages={"required":"Titel feltet er påkrævet."}
    )
    description = models.CharField(
        max_length=255,
        error_messages={"required":"Beskrivelsesfeltet er påkrævet."}
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("project-detail", kwargs={"pk": self.project.pk, "slug": self.project.slug})

    def __str__(self):
        return self.title


def get_upload_path(instance, filename):
    return os.path.join('img', str(instance.project.pk), filename)

class Media(models.Model):
    title = models.CharField(
        max_length=255,
        error_messages={"required":"Titel feltet er påkrævet."}
    )
    description = models.CharField(
        max_length=255,
        error_messages={"required":"Beskrivelsesfeltet er påkrævet."}
    )

    img = models.ImageField(upload_to=get_upload_path)

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("project-detail", kwargs={"pk": self.project.pk, "slug": self.project.slug})

    def __str__(self):
        return self.title
