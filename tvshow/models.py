from django.db import models
from datetime import datetime
from django.utils.text import slugify
from django.db.models import Q
from .utils.tvdb_api_wrap import download_image

# Create your models here.

class Show(models.Model):
    tvdbID = models.CharField(max_length=50)
    seriesName = models.CharField(max_length=50)
    overview = models.TextField()
    banner = models.CharField(max_length=150, null=True, blank=True)
    imbdID = models.CharField(max_length=50, null=True, blank=True)
    status_watched = models.BooleanField(default=False)
    slug = models.SlugField(null = True, blank = True)
    runningStatus = models.CharField(max_length=50)
    firstAired = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.seriesName

    def add_show(self, data, runningStatus):
        self.seriesName = data['seriesName']
        self.slug = slugify(self.seriesName)
        self.overview = data['overview']
        self.banner = download_image('http://thetvdb.com/banners/' + data['banner'], self.slug)
        self.imbdID = data['imdbID']
        self.tvdbID = data['tvdbID']
        self.runningStatus = runningStatus
        try:
            self.firstAired = datetime.strptime(data['firstAired'], '%Y-%m-%d').date()
        except:
            pass
        self.save()

    @property
    def episode_watch_count(self):
        return Episode.objects.filter(Q(season__show = self),Q(status_watched=True)).count()

    @property
    def total_episodes(self):
        return Episode.objects.filter(season__show = self).count()

class Season(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    number = models.IntegerField()
    status_watched = models.BooleanField(default = False)

    def __str__(self):
        showname = self.show.seriesName
        return_string = showname + " S" + str(self.number)
        return return_string

    def add_season(self, show, number):
        self.show = show
        self.number = number
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
    def episode_count(self):
        return Episode.objects.filter(season=self).count()

class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    episodeName = models.CharField(max_length=50)
    number = models.IntegerField()
    firstAired = models.DateField(null=True, blank = True)
    date_watched = models.DateField(null=True, blank=True)
    tvdbID = models.CharField(max_length=50)
    overview = models.TextField(null=True, blank=True)
    status_watched = models.BooleanField(default=False)

    def __str__(self):
        showname = self.season.show.seriesName
        return_string = showname + " S" + str(self.season.number) + "E" + str(self.number)
        return return_string

    def add_episode(self, season, data):
        self.season = season
        self.episodeName = data['episodeName']
        self.number = int(data['number'])
        try:
            self.firstAired = datetime.strptime(data['firstAired'], '%Y-%m-%d').date()
        except:
            pass
        self.tvdbID = data['tvdbID']
        try:
            self.overview = data['overview']
        except:
            pass
        self.save()

    def wst(self):
        self.status_watched = not(self.status_watched)
        self.save()
