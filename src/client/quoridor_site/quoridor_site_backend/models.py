from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wins = models.PositiveIntegerField(User, blank=True, null=True)
    losses = models.PositiveIntegerField(User, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def __int__(self):
        return self.wins + " " + self.losses

    def save(self):
        super().save()
