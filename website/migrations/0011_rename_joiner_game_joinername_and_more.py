# Generated by Django 4.0 on 2022-08-18 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_game_winner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='joiner',
            new_name='joinerName',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='owner',
            new_name='ownerName',
        ),
    ]
