from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
import random

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

    if hasattr(instance, 'profile'):
        instance.profile.save()

class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=255, default='AELAF MART')
    logo = models.ImageField(upload_to='site_branding/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site_branding/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Site Configuration'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # Ensure only one instance of SiteConfiguration exists
        if not self.pk and SiteConfiguration.objects.exists():
            return
        super(SiteConfiguration, self).save(*args, **kwargs)
