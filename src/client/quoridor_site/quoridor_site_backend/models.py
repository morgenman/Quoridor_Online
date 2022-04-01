from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wins = models.PositiveIntegerField(User, default=0)
    losses = models.PositiveIntegerField(User, default=0)

    def __str__(self):
        return self.user.username

    def __int__(self):
        return self.wins

    def __int__(self):
        return self.losses

    def save(self):
        super().save()


class Games(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    def __str__(self):
        return self.id
