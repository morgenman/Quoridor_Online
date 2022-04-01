from django.contrib import admin

# Register your models here.
from .models import Profile, Games


admin.site.register(Games)
admin.site.register(Profile)
