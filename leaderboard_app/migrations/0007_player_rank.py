# Generated by Django 3.0.7 on 2020-06-24 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard_app', '0006_auto_20200624_0159'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='rank',
            field=models.IntegerField(null=True),
        ),
    ]