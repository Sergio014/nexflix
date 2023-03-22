from django.db import models
from django.utils import timezone
from django.utils.text import slugify 
from django.db.models.signals import pre_save
from .db.models import PublishStateOptions
from .db.receivers import publish_state_pre_save, slugify_pre_save

# Create your models here.
class Video(models.Model):
	title = models.CharField(max_length=30)
	description= models.TextField()
	slug = models.SlugField(blank=True, null=True)
	video_id = models.CharField(max_length=30, unique=True)
	active = models.BooleanField()
	state = models.CharField(max_length=2, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT)
	publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	
	def get_playlist_ids(self):
		return self.playlist_set.all().values_list('id', flat=True)
	@property
	def Is_published(self):
		if self.active is False:
			return False
		state = self.state
		if state == PublishStateOptions.DRAFT:
			return False
		elif state == PublishStateOptions.PUBLISH:
			pub_timestamp = self.publish_timestamp
			now = timezone.now()
			if pub_timestamp is None:
				return False
			return pub_timestamp <= now
		return False

	def get_video_id(self):
		if not self.is_published:
			return None
		return self.video_id
	
	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
	
class VideoProxy(Video):
	class Meta:
		proxy = True
		verbose_name = 'Published Video'
		verbose_name_plural = 'Published Videos'

pre_save.connect(slugify_pre_save, sender=Video)
pre_save.connect(publish_state_pre_save, sender=Video)

pre_save.connect(slugify_pre_save, sender=VideoProxy)
pre_save.connect(publish_state_pre_save, sender=VideoProxy)
