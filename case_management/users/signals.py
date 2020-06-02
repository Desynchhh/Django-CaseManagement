from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Role, Profile
from django.contrib.auth.models import User


@receiver(pre_save, sender=Role)
def auto_insert_dates(sender, instance, *args, **kwargs):
    if instance.created_at is None:
        instance.created_at = timezone.now()
    if instance.updated_at is None:
        instance.updated_at = timezone.now()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance).save()
