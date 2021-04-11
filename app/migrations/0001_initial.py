# Generated by Django 2.2.20 on 2021-04-11 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HouseChore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='家事', max_length=100, verbose_name='家事')),
                ('description', models.TextField(blank=True, null=True, verbose_name='詳細')),
            ],
        ),
    ]
