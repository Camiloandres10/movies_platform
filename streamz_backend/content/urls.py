# content/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GenreViewSet, ContentViewSet

router = DefaultRouter()
router.register(r'genres', GenreViewSet)
router.register(r'content', ContentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]