# Generated by Django 4.0.3 on 2022-03-31 21:21

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wins', models.PositiveIntegerField(verbose_name=django.contrib.auth.models.User)),
            ],
        ),
    ]