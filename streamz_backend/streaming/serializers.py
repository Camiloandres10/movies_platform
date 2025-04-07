# streaming/serializers.py
from rest_framework import serializers
from .models import WatchHistory
from content.serializers import ContentSerializer, EpisodeSerializer
from .models import UserPreference
from content.serializers import GenreSerializer

class WatchHistorySerializer(serializers.ModelSerializer):
    content_details = ContentSerializer(source='content', read_only=True)
    episode_details = EpisodeSerializer(source='episode', read_only=True)
    
    class Meta:
        model = WatchHistory
        fields = ['id', 'content', 'episode', 'watched_time', 'watched_percentage', 
                  'watched_date', 'content_details', 'episode_details']
        read_only_fields = ['user', 'watched_date']
        
class UserPreferenceSerializer(serializers.ModelSerializer):
    genre_details = GenreSerializer(source='genre', read_only=True)
    
    class Meta:
        model = UserPreference
        fields = ['id', 'genre', 'score', 'genre_details']
        read_only_fields = ['user']