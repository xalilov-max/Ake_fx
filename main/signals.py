from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # Faqat oddiy foydalanuvchilar uchun Profile yaratish
    if created and not instance.is_superuser:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # Faqat oddiy foydalanuvchilar uchun Profile saqlash
    if hasattr(instance, 'profile') and not instance.is_superuser:
        instance.profile.save()