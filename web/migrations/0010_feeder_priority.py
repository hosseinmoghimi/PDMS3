# Generated by Django 3.2 on 2021-11-24 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_auto_20211125_0022'),
    ]

    operations = [
        migrations.AddField(
            model_name='feeder',
            name='priority',
            field=models.IntegerField(default=100, verbose_name='priority'),
        ),
    ]