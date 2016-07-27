from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from .utils.tvdb_api_wrap import search_series_list, get_series_with_id, get_all_episodes
from .models import Show,Season,Episode
from django.db.models import Q

# Create your views here.
def home(request):
    show_data = Show.objects.all()
    return render(request, 'tvshow/home.html', {'show_data':show_data})

@csrf_protect
def add(request):
    if request.method == 'POST':
        slug = ''
        tvdbID = request.POST.get('show_id')
        runningStatus = request.POST.get('runningStatus')
        show_data = get_series_with_id(int(tvdbID))
        if show_data is not None:
            show = Show()
            show.add_show(show_data, runningStatus)
            slug = show.slug
            seasons_data = get_all_episodes(int(tvdbID))
            for i in range(len(seasons_data)):
                string = 'Season' + str(i+1)
                season_data = seasons_data[string]
                season = Season()
                season.add_season(show, i+1)
                season_episodes_data = seasons_data[string]
                for season_episode in season_episodes_data:
                    if season_episode['episodeName']:
                        episode = Episode()
                        episode.add_episode(season, season_episode)
        return HttpResponseRedirect('/%s'%slug)
    return HttpResponseRedirect('/')


@csrf_protect
def add_search(request):
    context = {}
    context['Flag'] = False
    if request.method == 'POST':
        search_string = request.POST.get('search_string')
        show_datalist = search_series_list(search_string)
        if show_datalist is not None:
            context['Flag'] = True
            context['show_datalist'] = show_datalist
    return render(request, 'tvshow/add_search.html', {'context':context})

@csrf_protect
def single_show(request, show_slug):
    show = Show.objects.get(slug__iexact = show_slug)
    next_episode = Episode.objects.filter(Q(season__show=show),Q(status_watched=False)).first()
    return render(request, 'tvshow/single.html', {'show':show, 'next_episode':next_episode})

@csrf_protect
def episode_swt(request):
    if request.method == 'POST':
        episode_id = request.POST.get('episode_swt')
        episode = Episode.objects.get(id = episode_id)
        if episode:
            episode.wst()
            show = episode.season.show
            return HttpResponseRedirect('/%s'%show.slug)
    return HttpResponseRedirect('/')

@csrf_protect
def season_swt(request):
    if request.method == 'POST':
        season_id = request.POST.get('season_swt')
        season = Season.objects.get(id = season_id)
        if season:
            season.wst()
            show = season.show
            return HttpResponseRedirect('/%s'%show.slug)
    return HttpResponseRedirect('/')

def search(request):
    search_query = request.GET.get('query')
    show_list = Show.objects.filter(seriesName__icontains=search_query)
    if show_list and search_query:
        return render(request, 'tvshow/home.html', {'show_data':show_list})
    return HttpResponseRedirect('/')
