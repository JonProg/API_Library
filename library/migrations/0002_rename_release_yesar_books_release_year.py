# Generated by Django 4.2.5 on 2023-09-19 03:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='books',
            old_name='release_yesar',
            new_name='release_year',
        ),
    ]
