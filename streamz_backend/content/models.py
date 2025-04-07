from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Content(models.Model):
    CONTENT_TYPES = [
        ('movie', 'Película'),
        ('series', 'Serie'),
        ('documentary', 'Documental'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_year = models.IntegerField()
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    genres = models.ManyToManyField(Genre)
    thumbnail = models.URLField()
    video_file = models.URLField()
    min_subscription_plan = models.ForeignKey('authentication.SubscriptionPlan', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.title

class Episode(models.Model):
    series = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='episodes')
    title = models.CharField(max_length=200)
    episode_number = models.IntegerField()
    season_number = models.IntegerField()
    video_file = models.URLField()
    duration = models.IntegerField()  # en minutos
    
    def __str__(self):
        return f"{self.series.title} - S{self.season_number}E{self.episode_number} - {self.title}"