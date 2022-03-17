# Generated by Django 4.0.3 on 2022-03-02 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web2', '0003_feeder_register_power_factor_feeder_v_ab_feeder_v_ac_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='feeder',
            name='p',
            field=models.IntegerField(blank=True, null=True, verbose_name='p'),
        ),
        migrations.AddField(
            model_name='feeder',
            name='power_factor',
            field=models.IntegerField(blank=True, null=True, verbose_name='power_factor'),
        ),
        migrations.AddField(
            model_name='feeder',
            name='q',
            field=models.IntegerField(blank=True, null=True, verbose_name='q'),
        ),
        migrations.AddField(
            model_name='feeder',
            name='s',
            field=models.IntegerField(blank=True, null=True, verbose_name='s'),
        ),
    ]