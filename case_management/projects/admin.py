from django.contrib import admin

from .models import Project, Note, Media

# Register your models here.
admin.site.register(Project)
admin.site.register(Note)
admin.site.register(Media)