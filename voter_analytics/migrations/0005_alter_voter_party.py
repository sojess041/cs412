# Generated by Django 5.1.5 on 2025-04-04 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voter_analytics', '0004_alter_voter_options_alter_voter_party_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='party',
            field=models.CharField(max_length=2),
        ),
    ]
