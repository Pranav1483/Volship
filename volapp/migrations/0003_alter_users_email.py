# Generated by Django 5.0.1 on 2024-02-08 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volapp', '0002_users_lastpromptdone_users_maxstreak'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.CharField(max_length=500, unique=True),
        ),
    ]