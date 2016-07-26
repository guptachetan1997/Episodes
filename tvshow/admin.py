from django.contrib import admin
from .models import (Episode, Season, Show)
# Register your models here.
admin.site.register(Show)
admin.site.register(Season)
admin.site.register(Episode)
