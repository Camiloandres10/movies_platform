# streaming/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WatchHistoryViewSet, 
    UserPreferenceViewSet, 
    RecommendationsView,
    TrendingContentView
)

router = DefaultRouter()
router.register(r'history', WatchHistoryViewSet, basename='history')
router.register(r'preferences', UserPreferenceViewSet, basename='preferences')

urlpatterns = [
    path('', include(router.urls)),
    path('recommendations/', RecommendationsView.as_view(), name='recommendations'),
    path('trending/', TrendingContentView.as_view(), name='trending'),
]