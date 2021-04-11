# Generated by Django 2.2.13 on 2021-03-28 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210328_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='housechore_desc',
            field=models.CharField(default='詳細なし', max_length=100, verbose_name='詳細'),
        ),
        migrations.AlterField(
            model_name='user',
            name='housechore_title',
            field=models.CharField(default='割り当てられていません', max_length=100, verbose_name='家事'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='ユーザー', max_length=20, verbose_name='ユーザー名'),
        ),
    ]