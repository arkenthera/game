# Generated by Django 3.0.7 on 2020-06-25 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard_app', '0002_auto_20200624_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pointsubmission',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='leaderboard_app.Player'),
        ),
    ]
