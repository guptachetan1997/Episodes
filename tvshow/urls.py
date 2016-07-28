from django.conf.urls import url
from .views import (home, add_search, add ,single_show, episode_swt, season_swt, search)
urlpatterns = [
    url(r'^(?P<view_type>||all|unwatched|watched)$', home),
    url(r'^add_search', add_search),
    url(r'^add', add),
    url(r'^search', search, name='search'),
    url(r'^show/(?P<show_slug>[a-zA-Z0-9-]*$)', single_show),
    url(r'^episode_swt', episode_swt),
    url(r'^season_swt', season_swt),
]
