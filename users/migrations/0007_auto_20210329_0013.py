# Generated by Django 2.2.13 on 2021-03-28 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210328_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='created_at',
            field=models.DateTimeField(auto_now=True, verbose_name='作成日'),
        ),
        migrations.AlterField(
            model_name='house',
            name='name',
            field=models.CharField(default='House', max_length=20, verbose_name='ハウス名'),
        ),
    ]
