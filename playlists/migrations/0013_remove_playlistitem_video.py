# Generated by Django 4.1.3 on 2022-12-23 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0012_remove_playlist_videos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlistitem',
            name='video',
        ),
    ]
