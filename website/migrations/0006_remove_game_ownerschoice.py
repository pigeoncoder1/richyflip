# Generated by Django 4.0 on 2022-08-07 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_rename_ownerchoice_game_ownerschoice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='ownersChoice',
        ),
    ]
