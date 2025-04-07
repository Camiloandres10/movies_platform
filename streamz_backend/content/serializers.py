# content/serializers.py
from rest_framework import serializers
from .models import Genre, Content, Episode

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['id', 'title', 'season_number', 'episode_number', 'video_file', 'duration']

class ContentSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    
    class Meta:
        model = Content
        fields = ['id', 'title', 'description', 'release_year', 'content_type', 
                  'genres', 'thumbnail', 'video_file', 'min_subscription_plan']

class ContentDetailSerializer(ContentSerializer):
    episodes = EpisodeSerializer(many=True, read_only=True)
    
    class Meta(ContentSerializer.Meta):
        fields = ContentSerializer.Meta.fields + ['episodes']