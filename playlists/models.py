from django.db import models
from django.utils import timezone
from django.utils.text import slugify 
from django.db.models.signals import pre_save
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Avg, Max, Min, Q

from ratings.models import Rating
from tags.models import TaggedItem
from categories.models import Category
from videos.db.models import PublishStateOptions
from videos.db.receivers import publish_state_pre_save, slugify_pre_save, unique_slugify_pre_save
from videos.models import Video

class PlaylistQuerySet(models.QuerySet):
	def published(self):
		now = timezone.now()
		return self.filter(
			state = PublishStateOptions.PUBLISH,
			publish_timestamp__lte = now
		)

class PlaylistManager(models.Manager):
	def get_queryset(self):
		return PlaylistQuerySet(self.model, using=self._db)
	def published(self):
		return self.get_queryset().published()
	def featured_playlist(self):
		return self.get_queryset().filter(type=Playlist.PlaylistTypeChoices.PLAYLIST)

def pr_limit_choices_to():
	return {"type": Playlist.PlaylistTypeChoices.MOVIE}

class Playlist(models.Model):
	class PlaylistTypeChoices(models.TextChoices):
		MOVIE = "MOV", "Movie"
		SHOW = "TVS", "TV Show"
		SEASON = "SEA", "Season"
		PLAYLIST = "PLY", "Playlist"
		
	parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
	order = models.IntegerField(default=1)
	title = models.CharField(max_length=30)
	type = models.CharField(max_length=3, choices=PlaylistTypeChoices.choices, default=PlaylistTypeChoices.PLAYLIST)
	description= models.TextField()
	slug = models.SlugField(blank=True, null=True)
	video = models.ForeignKey(Video, null=True, on_delete=models.SET_NULL)
	videos = models.ManyToManyField(Video, blank=True, related_name='playlist_video')
	active = models.BooleanField()
	state = models.CharField(max_length=2, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT)
	publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
	tags = GenericRelation(TaggedItem, related_query_name='playlist')
	ratings = GenericRelation(Rating, related_query_name='playlist')
	related = models.ForeignKey("self", blank=True,  limit_choices_to=pr_limit_choices_to, null=True, on_delete=models.SET_NULL, related_name="me")
		
	objects = PlaylistManager()
	
	def get_short_display(self):
		return ''
	
	def get_playlist_avg(self):
		return Playlist.objects.filter(id=self.id).aggregate(Avg("ratings__value"))
		
	def get_playlist_spread(self):
		return Playlist.objects.filter(id=self.id).aggregate(max=Max("ratings__value"), min=Min("ratings__value"))
	
	def get_video_id(self):
		return self.video.get_video_id()
		
	def get_clips(self):
		return self.playlistitem_set.all(). published()
	
	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		
	def __str__(self):
		return self.title

class MovieProxyManager(PlaylistManager):
	def all(self):
		return self.get_queryset().filter(type=Playlist.PlaylistTypeChoices.MOVIE)
		
class MovieProxy(Playlist):
	objects = MovieProxyManager()
	class Meta:
		verbose_name = 'Movie'
		verbose_name_plural = 'Movies'
		proxy = True
	
	def get_movie_id(self):
		return self.get_video_id()
		
	def save(self, *args, **kwargs):
		self.type = Playlist.PlaylistTypeChoices.MOVIE
		super().save(*args, **kwargs)

class TVShowProxyManager(PlaylistManager):
	def all(self):
		return self.get_queryset().filter(parent__isnull=True, type=Playlist.PlaylistTypeChoices.SHOW)
		
class TVShowProxy(Playlist):
	objects = TVShowProxyManager()
	fk_name = 'playlist'
	class Meta:
		verbose_name = 'TV Show'
		verbose_name_plural = 'TV Shows'
		proxy = True
	
	@property
	def seasons(self):
		return self.playlist_set.published()
		
	def get_short_display(self):
		return f'{self.seasons.count()} Seasons'

	def save(self, *args, **kwargs):
		self.type = Playlist.PlaylistTypeChoices.SHOW
		super().save(*args, **kwargs)
		
class TVShowSeasonProxyManager(PlaylistManager):
	def all(self):
		return self.get_queryset().filter(parent__isnull=False, type=Playlist.PlaylistTypeChoices.SEASON)

class TVShowSeasonProxy(Playlist):
	objects = TVShowSeasonProxyManager()
	fk_name = 'playlist'
	class Meta:
		verbose_name = 'Season'
		verbose_name_plural = 'Seasons'
		proxy = True

	def get_episodes(self):
		return self.playlistitem_set.all(). published()
		
	def get_season_trailer(self):
		return self.get_video_id()

	def save(self, *args, **kwargs):
		self.type = Playlist.PlaylistTypeChoices.SEASON
		super().save(*args, **kwargs)

class PlaylistItemQuerySet(models.QuerySet):
	def published(self):
		now = timezone.now()
		return self.filter(
			playlist__state = PublishStateOptions.PUBLISH,
			playlist__publish_timestamp__lte = now,
			video__state = PublishStateOptions.PUBLISH,
			video__publish_timestamp__lte = now
		)

class PlaylistItemManager(models.Manager):
	def get_queryset(self):
		return PlaylistQuerySet(self.model, using=self._db)
	def published(self):
		return self.get_queryset().published()
	def featured_playlist(self):
		return self.get_queryset().filter(type=Playlist.PlaylistTypeChoices.PLAYLIST)

class PlaylistRelated(models.Model):
	playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
	order = models.IntegerField(default=1)
	timestamp = models.DateTimeField(auto_now_add=True)
		
class PlaylistItem(models.Model):
	playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
	order = models.IntegerField(default=1)
	timestamp = models.DateTimeField(auto_now_add=True)
	
	objects = PlaylistItemManager()
	class Meta:
		ordering = ['order', '-timestamp'] 

pre_save.connect(unique_slugify_pre_save, sender=Playlist)
pre_save.connect(publish_state_pre_save, sender=Playlist)

pre_save.connect(unique_slugify_pre_save, sender=MovieProxy)
pre_save.connect(publish_state_pre_save, sender=MovieProxy)

pre_save.connect(unique_slugify_pre_save, sender=TVShowProxy)
pre_save.connect(publish_state_pre_save, sender=TVShowProxy)

pre_save.connect(unique_slugify_pre_save, sender=TVShowSeasonProxy)
pre_save.connect(publish_state_pre_save, sender=TVShowSeasonProxy)