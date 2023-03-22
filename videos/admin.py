from django.contrib import admin

from .models import Video, VideoProxy
# Register your models here.

class VideoAdmin(admin.ModelAdmin):
	list_display = ['title', 'video_id']
	search_fields = ['title']
	list_filter = ['active']
	class Meta:
		model = Video

admin.site.register(Video, VideoAdmin)

class VideoProxyAdmin(admin.ModelAdmin):
	list_display = ['title', 'video_id']
	search_fields = ['title']
	list_filter = ['active']
	class Meta:
		model = VideoProxy

	def get_queryset(self, request):
		return VideoProxy.objects.filter(active=True)
		
admin.site.register(VideoProxy, VideoProxyAdmin)