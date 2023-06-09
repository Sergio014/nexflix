# Generated by Django 4.1.3 on 2022-12-23 10:22

from django.db import migrations, models
import django.db.models.deletion
import playlists.models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_rename_name_video_title_video_publish_timestamp_and_more'),
        ('playlists', '0003_playlist_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='videos',
            field=models.ManyToManyField(blank=True, related_name='playlist_item', through='playlists.PlaylistItem', to='videos.video'),
        ),
        migrations.CreateModel(
            name='PlaylistRelated',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=1)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playlists.playlist')),
                ('related', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_item', to='playlists.playlist')),
            ],
        ),
        migrations.AddField(
            model_name='playlist',
            name='related',
            field=models.ManyToManyField(blank=True, limit_choices_to=playlists.models.pr_limit_choices_to, related_name='related', through='playlists.PlaylistRelated', to='playlists.playlist'),
        ),
    ]
