# Generated by Django 4.0.3 on 2022-03-02 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web2', '0002_auto_20220221_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='feeder',
            name='register_power_factor',
            field=models.IntegerField(default=10, verbose_name='register_power_factor'),
        ),
        migrations.AddField(
            model_name='feeder',
            name='v_ab',
            field=models.IntegerField(blank=True, null=True, verbose_name='V ab'),
        ),
        migrations.AddField(
            model_name='feeder',
            name='v_ac',
            field=models.IntegerField(blank=True, null=True, verbose_name='V ac'),
        ),
        migrations.AddField(
            model_name='feeder',
            name='v_bc',
            field=models.IntegerField(blank=True, null=True, verbose_name='V bc'),
        ),
        migrations.AlterField(
            model_name='feeder',
            name='circuit_breaker_status',
            field=models.CharField(choices=[('OPEN', 'OPEN'), ('CLOSE', 'CLOSE'), ('TEST', 'TEST'), ('FAILED', 'FAILED'), ('TRIP', 'TRIP'), ('SERVICE', 'SERVICE')], default='TEST', max_length=50, verbose_name='circuit_breaker_status'),
        ),
    ]
