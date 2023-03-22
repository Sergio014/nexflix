from django.views.generic import ListView, DetailView
from django.http import Http404
from django.utils import timezone

from .models import MovieProxy, TVShowProxy, Playlist, TVShowSeasonProxy
from videos.db.models import PublishStateOptions

class PlaylistMixin():
	template_name = "playlist_list.html"
	title = None
	
	def get_queryset(self):
		return super().get_queryset().published()
		
	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		if self.title is not None:
			context['title'] = self.title
		return context

class FeaturedPlaylistListView(PlaylistMixin, ListView):
	title = "Featured"
	queryset = Playlist.objects.featured_playlist()

class MovieListView(PlaylistMixin, ListView):
	title = "Movies"
	queryset = MovieProxy.objects.all()
	
class MovieDetailView(DetailView):
	template_name = "playlists/movie_detail.html"
	queryset = MovieProxy.objects.all()

class PlaylistDetailView(DetailView):
	template_name = "playlists/playlist_detail.html"
	queryset = Playlist.objects.all()
	
class TVShowDetailView(DetailView):
	template_name = "playlists/tvshow_detail.html"
	queryset = TVShowProxy.objects.all()

class TVShowSeasonDetailView(DetailView):
	template_name = "playlists/tvshow_season_detail.html"
	queryset = TVShowSeasonProxy.objects.all()
	def get_object(self):
		kwargs = self.kwargs
		show_slug = kwargs.get("showSlug")
		season_slug = kwargs.get("seasonSlug")
		now = timezone.now()
		try:
			obj = TVShowSeasonProxy.objects.get(state=PublishStateOptions.PUBLISH, publish_timestamp__lte = now, parent__slug__iexact=show_slug, slug__iexact=season_slug)
		except TVShowSeasonProxy.MultipleObjectsReturned:
			qs = TVShowSeasonProxy.objects.get(state=PublishStateOptions.PUBLISH, publish_timestamp__lte = now, parent__slug__iexact=show_slug, slug__iexact=season_slug).published()
			obj = qs.first()
		except:
			raise Http404
		return obj
		#qs = self.get_queryset().filter(parent__slug__iexact=show_slug, slug__iexact=season_slug)
	#	if not qs.count() == 1:
	#		raise Http404
	#	return qs.first()

class TVShowListView(PlaylistMixin, ListView):
	title = "TVShow"
	queryset = TVShowProxy.objects.all()