from django.db import models
from authentication.models import User
from content.models import Content, Episode

class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, null=True)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, null=True)
    watched_time = models.IntegerField(default=0)  # tiempo en segundos
    watched_percentage = models.FloatField(default=0)
    watched_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-watched_date']
        
    def __str__(self):
        if self.episode:
            return f"{self.user.username} - {self.episode}"
        return f"{self.user.username} - {self.content.title}"

class UserPreference(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    genre = models.ForeignKey('content.Genre', on_delete=models.CASCADE)
    score = models.FloatField(default=0)  # Para calcular recomendaciones
    
    class Meta:
        unique_together = ('user', 'genre')