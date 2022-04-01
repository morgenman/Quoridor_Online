from django.contrib import admin

# Register your models here.
from .models import Profile, Game


admin.site.register(Game)
admin.site.register(Profile)
