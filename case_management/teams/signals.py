from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils import timezone

from projects.models import Project
from .models import Notification


@receiver(post_save, sender=Project)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(team=instance.team, project=instance).save()


@receiver(post_save, sender=Project)
def update_notification_read_at(sender, instance, **kwargs):
    notif = Notification.objects.get(project=instance)
    if instance.leader is None:
        notif.read_at = None
    else:
        notif.read_at = timezone.now()
    notif.save()
