from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

from .models import Project, Media
from blobstorage import AzureStorage

# @receiver(post_save, sender=Project)
# def create_azure_storage_container(instance, created, **kwargs):
#     if created:
#         # Save container name in DB
#         instance.azure_container = f'project-{instance.pk}'
#         instance.save()

#         # Create container on Azure
#         azure = AzureStorage()
#         azure.create_container(instance.azure_container)


# @receiver(pre_delete, sender=Project)
# def delete_azure_storage_container(instance, **kwargs):
#     azure = AzureStorage()
#     azure.delete_container(instance.azure_container)


# @receiver(pre_delete, sender=Media)
# def delete_blob(instance, **kwargs):
#     azure = AzureStorage()
#     azure.delete_blob(instance.project.azure_container, instance.blob)
