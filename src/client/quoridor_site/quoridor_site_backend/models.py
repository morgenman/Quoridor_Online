from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wins = models.PositiveIntegerField(User, default=1)
    losses = models.PositiveIntegerField(User, default=1)

    def __str__(self):
        return self.user.username

    def __int__(self):
        return self.wins + " " + self.losses

    def save(self):
        super().save()
