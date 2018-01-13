# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-02 13:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tvshow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='episode',
            name='siteRating',
        ),
        migrations.AddField(
            model_name='show',
            name='genre_list',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='show',
            name='last_updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='show',
            name='modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='show',
            name='network',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='show',
            name='siteRating',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='show',
            name='userRating',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='episode',
            name='date_watched',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='episode',
            name='episodeName',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='episode',
            name='overview',
            field=models.TextField(blank=True, null=True),
        ),
    ]
