from django.contrib import admin
from .models import WatchHistory, UserPreference

admin.site.register(WatchHistory)
admin.site.register(UserPreference)