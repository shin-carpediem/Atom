# Generated by Django 3.0.14 on 2021-05-01 01:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_requestchhouse'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestHouseOwner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='日付')),
                ('house', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='users.House')),
            ],
        ),
    ]
