from django.contrib import admin

from playlists.models import Playlist, PlaylistItem, TVShowProxy, TVShowSeasonProxy, MovieProxy, PlaylistRelated
from tags.admin import TaggedItemInline

class MovieProxyAdmin(admin.ModelAdmin):
	fields = ["title", "description", "state", "video", "slug", "active", "category"]
	class Meta:
		model = MovieProxy
	def get_queryset(self, request):
		return MovieProxy.objects.all()
		
admin.site.register(MovieProxy, MovieProxyAdmin)

class SeasonEpisodeInline(admin.TabularInline):
	model = PlaylistItem
	extra = 0
	
class TVShowSeasonProxyAdmin(admin.ModelAdmin):
	inlines = [SeasonEpisodeInline]
	list_display = ["title", "parent"]
	class Meta:
		model = TVShowSeasonProxy
	def get_queryset(self, request):
		return TVShowSeasonProxy.objects.all()

admin.site.register(TVShowSeasonProxy, TVShowSeasonProxyAdmin)

class TVShowSeasonProxyInline(admin.TabularInline):
	model = TVShowSeasonProxy
	fk_name = 'parent'
	extra = 0
	fields = ["order", "title", "state", "active"]
	
class TVShowProxyAdmin(admin.ModelAdmin):
	inlines = [TaggedItemInline, TVShowSeasonProxyInline]
	fields = ["title", "description", "state", "video", "slug", "active", "category"]
	list_display = ["title"]
	class Meta:
		model = TVShowProxy
	def get_queryset(self, request):
		return TVShowProxy.objects.all()
	
class PlaylistItemInline(admin.TabularInline):
	model = PlaylistItem
	extra = 0

class PlaylistRelatedInline(admin.TabularInline):
	model = PlaylistRelated
	extra = 0	
	
class PlaylistAdmin(admin.ModelAdmin):
	inlines = [PlaylistItemInline, PlaylistRelatedInline]
	fields = ["title", "type" "description", "state", "video", "slug", "active", "category"]
	class Meta:
		model = Playlist
	def get_queryset(self, request):
		return Playlist.objects.filter(type=Playlist.PlaylistTypeChoices.PLAYLIST)

admin.site.register(TVShowProxy, TVShowProxyAdmin)
admin.site.register(Playlist, PlaylistAdmin)