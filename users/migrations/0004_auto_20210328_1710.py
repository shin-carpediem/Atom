# Generated by Django 2.2.13 on 2021-03-28 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210327_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='house',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='users.House'),
        ),
    ]
