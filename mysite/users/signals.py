from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from users.models import ProfileModel

@receiver(post_save, sender=User)
def build_profile(sender, instance, created, **kwargs):
    if created:
        ProfileModel.objects.create(profile_username=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profilemodel.save()        
        