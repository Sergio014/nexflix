# Generated by Django 4.1.3 on 2022-12-23 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0011_alter_playlist_videos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlist',
            name='videos',
        ),
    ]
