from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from .utils.get_omdbapi import get_full_season_data
from .models import Show,Season,Episode
from django.db.models import Q

# Create your views here.
def home(request):
    show_data = Show.objects.all()
    return render(request, 'tvshow/home.html', {'show_data':show_data})

@csrf_protect
def add(request):
    context = {}
    context['Flag'] = False
    if request.method == 'POST':
        search_string = request.POST.get('search_string')
        show_data = get_full_season_data(search_string)
        if show_data is not None:
            context['Title'] = show_data['Title']
            context['Poster'] = show_data['Poster']
            context['Plot'] = show_data['Plot']
            context['Flag'] = True
            show = Show()
            show.add_show(show_data)
            seasons_data = show_data['Episode_data']
            for i in range(int(show_data['totalSeasons'])):
                string = 'Season' + str(i+1)
                season_data = seasons_data[string]
                season = Season()
                season.add_season(show, season_data)
                season_episodes_data = season_data['Episodes']
                for season_episode in season_episodes_data:
                    episode = Episode()
                    episode.add_episode(season, season_episode)

    return render(request, 'tvshow/add.html', {'context':context})

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
