# Generated by Django 4.0.3 on 2022-04-01 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quoridor_site_backend', '0004_alter_profile_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Games',
            new_name='Game',
        ),
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='losses',
            field=models.PositiveIntegerField(default=0, verbose_name='loss'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='wins',
            field=models.PositiveIntegerField(default=0, verbose_name='win'),
        ),
    ]
