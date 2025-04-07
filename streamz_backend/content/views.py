# content/views.py
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Genre, Content, Episode
from .serializers import GenreSerializer, ContentSerializer, ContentDetailSerializer, EpisodeSerializer
from .permissions import HasActiveSubscription
from django.conf import settings
from rest_framework.permissions import IsAuthenticated, AllowAny

class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class ContentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['content_type', 'release_year', 'genres']
    search_fields = ['title', 'description']
    permission_classes = [AllowAny]
    
    def get_queryset(self):
    # Modificación para desarrollo - muestra todo el contenido
        if settings.DEBUG:
            return Content.objects.all()
    
    # Comportamiento original - filtrar por plan
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'plan') and user.plan:
            return Content.objects.filter(min_subscription_plan__price__lte=user.plan.price)
        return Content.objects.none()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ContentDetailSerializer
        return ContentSerializer
    
    @action(detail=False, methods=['get'])
    def movies(self, request):
        movies = self.get_queryset().filter(content_type='movie')
        page = self.paginate_queryset(movies)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def series(self, request):
        series = self.get_queryset().filter(content_type='series')
        page = self.paginate_queryset(series)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def documentaries(self, request):
        docs = self.get_queryset().filter(content_type='documentary')
        page = self.paginate_queryset(docs)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)