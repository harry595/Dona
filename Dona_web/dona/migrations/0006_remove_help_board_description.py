# Generated by Django 3.1 on 2020-11-18 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dona', '0005_help_board_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='help_board',
            name='description',
        ),
    ]