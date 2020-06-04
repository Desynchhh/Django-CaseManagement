# Generated by Django 3.0.6 on 2020-06-04 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0004_remove_team_projects'),
        ('projects', '0004_remove_project_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='team',
            field=models.ForeignKey(blank=True, default=None, help_text='blah', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='teams.Team'),
        ),
    ]
