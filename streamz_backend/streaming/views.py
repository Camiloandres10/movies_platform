# streaming/views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import WatchHistory
from .serializers import WatchHistorySerializer, UserPreferenceSerializer
from rest_framework import generics
from django.db.models import Count, F, Q, Value, FloatField
from django.db.models.functions import Coalesce
from content.models import Content, Genre
from content.serializers import ContentSerializer
from .models import UserPreference
from datetime import datetime, timedelta
from django.db.models import Case, When

class WatchHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = WatchHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Devuelve solo el historial del usuario actual
        return WatchHistory.objects.filter(user=self.request.user).order_by('-watched_date')
    
    def perform_create(self, serializer):
        # Asigna automáticamente el usuario actual al crear un registro
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        # Asegura que se actualice solo el historial del usuario actual
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def continue_watching(self, request):
        # Obtener contenido que el usuario ha comenzado pero no terminado
        continue_watching = self.get_queryset().filter(
            watched_percentage__lt=90,  # No completado
            watched_percentage__gt=0    # Comenzado
        ).order_by('-watched_date')[:10]
        
        serializer = self.get_serializer(continue_watching, many=True)
        return Response(serializer.data)
        
    @action(detail=False, methods=['get'])
    def recent(self, request):
        # Obtener el historial reciente, independientemente del porcentaje visto
        recent = self.get_queryset()[:20]
        serializer = self.get_serializer(recent, many=True)
        return Response(serializer.data)
    
    # Añade esto a streaming/views.py dentro de WatchHistoryViewSet
    @action(detail=False, methods=['post'])
    def update_progress(self, request):
        content_id = request.data.get('content')
        episode_id = request.data.get('episode')
        watched_time = request.data.get('watched_time')
        total_duration = request.data.get('total_duration')
    
        if not content_id and not episode_id:
            return Response({"error": "Se requiere content_id o episode_id"}, status=400)
    
        if not watched_time:
            return Response({"error": "Se requiere watched_time"}, status=400)
    
        # Calcular el porcentaje visto
        watched_percentage = 0
        if total_duration and float(total_duration) > 0:
            watched_percentage = (float(watched_time) / float(total_duration)) * 100
    
        # Buscar un registro existente o crear uno nuevo
        history, created = WatchHistory.objects.get_or_create(
            user=request.user,
            content_id=content_id if content_id else None,
            episode_id=episode_id if episode_id else None,
            defaults={
                'watched_time': watched_time,
                'watched_percentage': watched_percentage
            }
        )
    
        # Si el registro ya existía, actualiza los campos
        if not created:
            history.watched_time = watched_time
            history.watched_percentage = watched_percentage
            history.save()
    
        serializer = self.get_serializer(history)
        return Response(serializer.data)


class RecommendationsView(generics.ListAPIView):
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # 1. Obtener todos los contenidos que el usuario ha visto
        watched_content_ids = WatchHistory.objects.filter(
            user=user
        ).values_list('content', flat=True).distinct()
        
        # 2. Obtener los géneros preferidos del usuario basado en su historial
        genre_preferences = {}
        
        # 2.1 Géneros de contenido completamente visto (alta preferencia)
        completed_content_genres = WatchHistory.objects.filter(
            user=user, 
            watched_percentage__gte=90
        ).values_list('content__genres', flat=True)
        
        for genre_id in completed_content_genres:
            if genre_id:
                genre_preferences[genre_id] = genre_preferences.get(genre_id, 0) + 3
        
        # 2.2 Géneros de contenido parcialmente visto
        partial_content_genres = WatchHistory.objects.filter(
            user=user, 
            watched_percentage__lt=90,
            watched_percentage__gt=20
        ).values_list('content__genres', flat=True)
        
        for genre_id in partial_content_genres:
            if genre_id:
                genre_preferences[genre_id] = genre_preferences.get(genre_id, 0) + 1
        
        # 2.3 También usar preferencias guardadas si existen
        saved_preferences = UserPreference.objects.filter(
            user=user
        ).values_list('genre_id', 'score')
        
        for genre_id, score in saved_preferences:
            genre_preferences[genre_id] = genre_preferences.get(genre_id, 0) + score
        
        # 3. Ordenar los géneros por preferencia
        sorted_genres = sorted(
            genre_preferences.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        top_genre_ids = [genre_id for genre_id, _ in sorted_genres[:5]]
        
        # 4. Recomendar contenido basado en géneros preferidos que no haya visto
        if top_genre_ids:
            recommendations = Content.objects.filter(
                genres__in=top_genre_ids
            ).exclude(
                id__in=watched_content_ids
            ).annotate(
                genre_match_count=Count('genres', filter=Q(genres__in=top_genre_ids))
            ).order_by('-genre_match_count', '-release_year')[:20]
            
            return recommendations
        
        # Si no hay suficientes datos, recomendar contenido popular
        return Content.objects.exclude(
            id__in=watched_content_ids
        ).order_by('-release_year')[:20]
        

class UserPreferenceViewSet(viewsets.ModelViewSet):
    serializer_class = UserPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserPreference.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def like_genre(self, request):
        genre_id = request.data.get('genre_id')
        if not genre_id:
            return Response({'error': 'Se requiere genre_id'}, status=400)
        
        preference, created = UserPreference.objects.get_or_create(
            user=request.user,
            genre_id=genre_id,
            defaults={'score': 5.0}
        )
        
        if not created:
            preference.score += 1
            preference.save()
        
        return Response({'status': 'success', 'preference': UserPreferenceSerializer(preference).data})
    
    @action(detail=False, methods=['post'])
    def dislike_genre(self, request):
        genre_id = request.data.get('genre_id')
        if not genre_id:
            return Response({'error': 'Se requiere genre_id'}, status=400)
        
        preference, created = UserPreference.objects.get_or_create(
            user=request.user,
            genre_id=genre_id,
            defaults={'score': -1.0}
        )
        
        if not created:
            preference.score -= 1
            preference.save()
        
        return Response({'status': 'success', 'preference': UserPreferenceSerializer(preference).data})
    
class TrendingContentView(generics.ListAPIView):
    serializer_class = ContentSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        # Contenido con más vistas en la última semana
        one_week_ago = datetime.now() - timedelta(days=7)
        
        trending_ids = WatchHistory.objects.filter(
            watched_date__gte=one_week_ago
        ).values('content').annotate(
            view_count=Count('content')
        ).order_by('-view_count').values_list('content', flat=True)[:20]
        
        # Preservar el orden de trending_ids
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(trending_ids)])
        return Content.objects.filter(id__in=trending_ids).order_by(preserved)