from tabnanny import verbose
from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns


# Create your models here.
class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, max_length=50)
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, max_length=50)
    player1 = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="player1_set", max_length=190
    )
    player2 = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="player2_set", max_length=190
    )
    state = models.CharField(max_length=100, default=" / / e1 e9 / 10 10 / 1")
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("game-detail", args=[str(self.id)])

    def get_player_turn(self, player):
        if player == str(self.player1.id):
            return "1"
        if player == str(self.player2.id):
            return "2"
        else:
            return "0"

    def get_date(self):
        out = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return out

    def get_players(self):
        out = self.player1.user.username + " vs " + self.player2.user.username
        return out

    def __str__(self):
        return str(self.id)
