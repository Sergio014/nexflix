# Generated by Django 4.1.3 on 2022-12-18 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('videos', '0004_rename_name_video_title_video_publish_timestamp_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=1)),
                ('title', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('slug', models.SlugField(blank=True, null=True)),
                ('active', models.BooleanField()),
                ('state', models.CharField(choices=[('PU', 'Publish'), ('DR', 'Draft')], default='DR', max_length=2)),
                ('publish_timestamp', models.DateTimeField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='playlists.playlist')),
                ('video', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='videos.video')),
                ('videos', models.ManyToManyField(blank=True, related_name='playlist_item', to='videos.video')),
            ],
        ),
        migrations.CreateModel(
            name='PlaylistItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=1)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playlists.playlist')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos.video')),
            ],
            options={
                'ordering': ['order', '-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='TVShowProxy',
            fields=[
            ],
            options={
                'verbose_name': 'TV Show',
                'verbose_name_plural': 'TV Shows',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('playlists.playlist',),
        ),
        migrations.CreateModel(
            name='TVShowSeasonProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Season',
                'verbose_name_plural': 'Seasons',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('playlists.playlist',),
        ),
    ]
