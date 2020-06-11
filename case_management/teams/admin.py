from django.contrib import admin

from .models import Team, Notification

# Register your models here.
admin.site.register(Team)
admin.site.register(Notification)