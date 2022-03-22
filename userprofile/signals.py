from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    '''
        Signal for creating UserProfile
    '''

    if created:
        UserProfile.objects.create(user=instance, id=instance.id)
        instance.userprofile.save()
