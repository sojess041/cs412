# Generated by Django 5.1.5 on 2025-02-20 00:46

from django.db import migrations, models
from django.db import models



class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profilepic',
            field=models.URLField(blank=True),
        ),
    ]