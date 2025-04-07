# streaming/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import WatchHistory, UserPreference

@receiver(post_save, sender=WatchHistory)
def update_user_preferences(sender, instance, created, **kwargs):
    """
    Actualiza automáticamente las preferencias del usuario cuando ve contenido
    """
    if not instance.content:
        return  # No actualizar si no hay contenido (sólo episodio)
    
    # Obtener los géneros del contenido
    genres = instance.content.genres.all()
    
    for genre in genres:
        # Incrementar la puntuación basada en el porcentaje visto
        score_increment = 0
        
        if instance.watched_percentage >= 90:
            # Si completó el contenido, mayor incremento
            score_increment = 2.0
        elif instance.watched_percentage >= 50:
            # Si vio la mitad, incremento medio
            score_increment = 1.0
        elif instance.watched_percentage >= 20:
            # Si vio al menos un poco, pequeño incremento
            score_increment = 0.5
            
        if score_increment > 0:
            preference, created = UserPreference.objects.get_or_create(
                user=instance.user,
                genre=genre,
                defaults={'score': score_increment}
            )
            
            if not created:
                # Limitar el score máximo
                new_score = min(preference.score + score_increment, 10.0)
                preference.score = new_score
                preference.save()