from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from timeEntries.models import TimeEntry

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def has_active_time_entry(self):
        return True if TimeEntry.objects.exclude(end_time__isnull=False).filter(owner = self.user) else False

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()