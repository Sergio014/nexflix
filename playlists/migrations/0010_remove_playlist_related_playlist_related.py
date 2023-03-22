# Generated by Django 4.1.3 on 2022-12-23 11:03

from django.db import migrations, models
import django.db.models.deletion
import playlists.models


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0009_alter_playlist_related'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlist',
            name='related',
        ),
        migrations.AddField(
            model_name='playlist',
            name='related',
            field=models.ForeignKey(blank=True, limit_choices_to=playlists.models.pr_limit_choices_to, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='me', to='playlists.playlist'),
        ),
    ]
