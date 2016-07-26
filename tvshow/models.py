from django.db import models
from datetime import datetime
from django.utils.text import slugify
from django.db.models import Q
from .utils.get_omdbapi import download_image

# Create your models here.

class Show(models.Model):
    title = models.CharField(max_length=50)
    plot = models.TextField()
    poster = models.CharField(max_length=150)
    total_seasons = models.IntegerField()
    imbdID = models.CharField(max_length=50)
    status_watched = models.BooleanField(default=False)
    slug = models.SlugField(null = True, blank = True)

    def __str__(self):
        return self.title

    def add_show(self, data):
        self.title = data['Title']
        self.slug = slugify(self.title)
        self.plot = data['Plot']
        self.poster = download_image(data['Poster'], self.slug)
        self.total_seasons = data['totalSeasons']
        self.imbdID = data['imdbID']
        self.save()

    @property
    def episode_watch_count(self):
        count = 0
        for season in self.season_set.all():
            count += season.watch_count
        return count

    @property
    def total_episodes(self):
        return Episode.objects.filter(season__show = self).count()

class Season(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    number = models.IntegerField()
    episode_count = models.IntegerField()
    status_watched = models.BooleanField(default = False)

    def __str__(self):
        showname = self.show.title
        return_string = showname + " S" + str(self.number)
        return return_string

    def add_season(self, show, data):
        self.show = show
        self.number = int(data['Season'])
        self.episode_count = data['count']
        self.save()

    def wst(self):
        if self.status_watched == True:
            for episode in self.episode_set.all():
                episode.status_watched = False
                episode.save()
            self.status_watched = False
            self.save()
        else:
            for episode in self.episode_set.all():
                episode.status_watched = True
                episode.save()
            self.status_watched = True
            self.save()

    @property
    def watch_count(self):
        return Episode.objects.filter(Q(season=self),Q(status_watched=True)).count()

    @property
    def total_count(self):
        return Episode.objects.filter(season=self).count()

class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    number = models.IntegerField()
    release_date = models.DateField(null=True, blank = True)
    date_watched = models.DateField(null=True, blank=True)
    imdbID = models.CharField(max_length=50)
    imdbRating = models.CharField(max_length=50, default='N/A')
    status_watched = models.BooleanField(default=False)

    def __str__(self):
        showname = self.season.show.title
        return_string = showname + " S" + str(self.season.number) + "E" + str(self.number)
        return return_string

    def add_episode(self, season, data):
        self.season = season
        self.title = data['Title']
        self.number = int(data['Episode'])
        try:
            self.release_date = datetime.strptime(data['Released'], '%Y-%m-%d').date()
        except:
            pass
        self.imdbID = data['imdbID']
        self.imdbRating = data['imdbRating']
        self.save()

    def wst(self):
        self.status_watched = not(self.status_watched)
        self.save()
