# Generated by Django 4.0.2 on 2022-04-07 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quoridor_site_backend', '0008_alter_profile_losses_alter_profile_wins'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(to='quoridor_site_backend.Profile'),
        ),
        migrations.AddField(
            model_name='game',
            name='state',
            field=models.CharField(default=' / / e1 e9 / 10 10 / 1', max_length=100),
        ),
    ]
