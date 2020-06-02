from django.db import models

from django.utils import timezone
from django.utils.text import slugify

# Create your models here.
class Team(models.Model):
    name = models.CharField(
        max_length = 255,
        help_text="Et beskrivende navn til dit hold.",
        error_messages={"required": "Navnefeltet er påkrævet."}
    )
    description = models.CharField(
        max_length = 255,
        help_text="En lille beskrivelse af dit holds funktion.",
        error_messages={"required": "Beskrivelsesfeltet er påkrævet."}
    )
    slug = models.SlugField(max_length=255, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self):
        self.slug = slugify(self.name)
        super().save()

    def __str__(self):
        return self.name