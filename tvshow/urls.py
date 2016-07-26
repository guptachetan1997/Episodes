from django.conf.urls import url
from .views import (home, add, single_show, episode_swt, season_swt)
urlpatterns = [
    url(r'^$', home),
    url(r'^add', add),
    url(r'^(?P<show_slug>[a-zA-Z0-9-]*$)', single_show),
    url(r'^episode_swt', episode_swt),
    url(r'^season_swt', season_swt),
]
