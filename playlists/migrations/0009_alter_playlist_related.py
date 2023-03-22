# Generated by Django 4.1.3 on 2022-12-23 10:48

from django.db import migrations, models
import playlists.models


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0008_alter_playlist_videos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='related',
            field=models.ManyToManyField(blank=True, limit_choices_to=playlists.models.pr_limit_choices_to, to='playlists.playlist'),
        ),
    ]
