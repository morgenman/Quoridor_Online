from tabnanny import verbose
from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wins = models.PositiveIntegerField(default=0, verbose_name="wins")
    losses = models.PositiveIntegerField(default=0, verbose_name="losses")

    def __str__(self):
        return self.user.username

    def get_wins(self):
        return self.wins

    def get_losses(self):
        return self.losses


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, max_length=5)
    players = models.ManyToManyField(Profile)
    state = models.CharField(max_length=100, default=" / / e1 e9 / 10 10 / 1")

    def get_absolute_url(self):
        return reverse("game-detail", args=[str(self.id)])

    def __str__(self):
        return str(self.id)
