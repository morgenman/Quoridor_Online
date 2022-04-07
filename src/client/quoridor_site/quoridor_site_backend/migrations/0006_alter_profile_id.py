# Generated by Django 4.0.3 on 2022-04-01 16:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('quoridor_site_backend', '0005_rename_games_game_alter_profile_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]