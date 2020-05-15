# Generated by Django 3.0.5 on 2020-04-25 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tvdbID', models.CharField(max_length=50)),
                ('seriesName', models.CharField(max_length=100)),
                ('overview', models.TextField()),
                ('banner', models.CharField(blank=True, max_length=150, null=True)),
                ('imbdID', models.CharField(blank=True, max_length=50, null=True)),
                ('status_watched', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('runningStatus', models.CharField(max_length=50)),
                ('firstAired', models.DateField(blank=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('siteRating', models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=5, null=True)),
                ('userRating', models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=5, null=True)),
                ('network', models.CharField(blank=True, max_length=50, null=True)),
                ('genre_list', models.TextField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('status_watched', models.BooleanField(default=False)),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tvshow.Show')),
            ],
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('episodeName', models.CharField(blank=True, max_length=100, null=True)),
                ('number', models.IntegerField()),
                ('firstAired', models.DateField(blank=True, null=True)),
                ('date_watched', models.DateField(auto_now=True, null=True)),
                ('tvdbID', models.CharField(max_length=50)),
                ('overview', models.TextField(blank=True, null=True)),
                ('status_watched', models.BooleanField(default=False)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tvshow.Season')),
            ],
        ),
    ]
