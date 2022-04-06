from tabnanny import verbose
from django.db import models
import uuid
from django.contrib.auth.models import User

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


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, max_length=5)

    def __str__(self):
        return self.id
