from django.db import models
from django.contrib.auth.models import AbstractUser

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50)  # básico, estándar, premium
    price = models.DecimalField(max_digits=6, decimal_places=2)
    max_screens = models.IntegerField(default=1)
    video_quality = models.CharField(max_length=20)  # SD, HD, 4K
    
    def __str__(self):
        return self.name

class User(AbstractUser):
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    subscription_active = models.BooleanField(default=True)
    subscription_end_date = models.DateField(null=True)
