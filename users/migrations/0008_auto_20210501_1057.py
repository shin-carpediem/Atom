# Generated by Django 3.0.14 on 2021-05-01 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20210501_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='inquire',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='email'),
        ),
        migrations.AddField(
            model_name='requestchhouse',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='email'),
        ),
    ]
