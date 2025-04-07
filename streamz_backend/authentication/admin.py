from django.contrib import admin
from .models import User, SubscriptionPlan

admin.site.register(SubscriptionPlan)
admin.site.register(User)