# Generated by Django 4.0 on 2022-08-21 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_game_joinerchoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='side',
            field=models.CharField(default='', max_length=100),
        ),
    ]