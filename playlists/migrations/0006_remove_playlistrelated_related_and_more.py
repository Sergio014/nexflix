# Generated by Django 4.1.3 on 2022-12-23 10:34

from django.db import migrations, models
import playlists.models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_rename_name_video_title_video_publish_timestamp_and_more'),
        ('playlists', '0005_alter_playlist_related_alter_playlist_videos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlistrelated',
            name='related',
        ),
        migrations.AlterField(
            model_name='playlist',
            name='related',
            field=models.ManyToManyField(blank=True, limit_choices_to=playlists.models.pr_limit_choices_to, related_name='related', through='playlists.PlaylistRelated', to='playlists.playlist'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='videos',
            field=models.ManyToManyField(blank=True, related_name='playlist_item', through='playlists.PlaylistItem', to='videos.video'),
        ),
    ]
