# Generated by Django 5.0.1 on 2024-02-24 09:24

import volapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volapp', '0005_remove_users_lastpromptdone_posts_answers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='answers',
            field=models.JSONField(default=volapp.models.default_answers),
        ),
        migrations.AlterField(
            model_name='posts',
            name='emotions',
            field=models.JSONField(default=volapp.models.default_emotions),
        ),
    ]
