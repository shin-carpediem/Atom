# Generated by Django 3.0.14 on 2021-05-01 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210501_1055'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requestchhouse',
            old_name='house',
            new_name='current_house',
        ),
        migrations.RenameField(
            model_name='requesthouseowner',
            old_name='current_house',
            new_name='house',
        ),
        migrations.RemoveField(
            model_name='requesthouseowner',
            name='request_house',
        ),
        migrations.AddField(
            model_name='requestchhouse',
            name='request_house',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='希望するハウス'),
        ),
    ]