from django.db import models

from django.shortcuts import reverse

from django.utils import timezone
from django.utils.text import slugify

# Create your models here.
class Team(models.Model):
    name = models.CharField(
        max_length = 255,
        unique=True,
        help_text="Et beskrivende navn til dit hold. Dette er navnet kunder og kollegaer vil se, når de vil oprette et projekt til dig.",
        error_messages={"required": "Navnefeltet er påkrævet."}
    )
    description = models.CharField(
        max_length = 255,
        help_text="En lille beskrivelse af dit holds funktion.",
        error_messages={"required": "Beskrivelsesfeltet er påkrævet."}
    )
    slug = models.SlugField(
        max_length=255,
        blank=True,
        help_text='Dette felt vil automatisk blive udfyldt når du opretter holdet.'
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("team-detail", kwargs={"pk": self.pk, "slug": self.slug})

    def __str__(self):
        return self.name


# Manager to return custom querysets from a table
class NotificationManager(models.Manager):
    def get_unread(self):
        return self.filter(read_at=None)        

class Notification(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    project = models.OneToOneField("projects.Project", on_delete=models.CASCADE)

    read_at = models.DateTimeField(blank=True, null=True, default=None)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Set model's manager to the custom manager
    objects = NotificationManager()

    def __str__(self):
        return f'({self.project.name}, {self.team.name})'
