# Generated by Django 3.2 on 2021-11-10 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=50, verbose_name='region')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('gps', models.CharField(blank=True, max_length=50, null=True, verbose_name='gps')),
            ],
            options={
                'verbose_name': 'Area',
                'verbose_name_plural': 'Areas',
            },
        ),
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('tip', models.CharField(blank=True, choices=[('MEDIUM_VOLTAGE', 'MEDIUM_VOLTAGE'), ('LOW_VOLTAGE', 'LOW_VOLTAGE'), ('HIGH_VOLTAGE', 'HIGH_VOLTAGE')], max_length=50, null=True, verbose_name='tip')),
                ('brand', models.CharField(blank=True, max_length=5000, null=True, verbose_name='brand')),
                ('model_name', models.CharField(blank=True, max_length=5000, null=True, verbose_name='model_name')),
                ('serial_no', models.CharField(blank=True, max_length=5000, null=True, verbose_name='serial_no')),
                ('description', models.CharField(blank=True, max_length=5000, null=True, verbose_name='description')),
                ('is_live', models.BooleanField(default=True, verbose_name='is live ?')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.area', verbose_name='area')),
            ],
            options={
                'verbose_name': 'Bus',
                'verbose_name_plural': 'Buses',
            },
        ),
        migrations.CreateModel(
            name='ComServer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('ip1', models.CharField(default='192.168.1.254', max_length=50, verbose_name='ip1')),
                ('port1', models.CharField(default='502', max_length=50, verbose_name='port1')),
                ('ip2', models.CharField(default='192.168.2.254', max_length=50, verbose_name='ip2')),
                ('port2', models.CharField(default='8080', max_length=50, verbose_name='port2')),
                ('username', models.CharField(default='root', max_length=50, verbose_name='username')),
                ('password', models.CharField(default='root', max_length=50, verbose_name='password')),
                ('redundancy', models.CharField(choices=[('HOT', 'HOT'), ('STAND_BY', 'STAND_BY')], default='HOT', max_length=50, verbose_name='redundancy')),
            ],
            options={
                'verbose_name': 'ComServer',
                'verbose_name_plural': 'ComServers',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
            },
        ),
        migrations.CreateModel(
            name='InputOutput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('register', models.IntegerField(verbose_name='register')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('com_server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.comserver', verbose_name='com_server')),
            ],
            options={
                'verbose_name': 'InputOutput',
                'verbose_name_plural': 'InputOutputs',
            },
        ),
        migrations.CreateModel(
            name='AnalogInput',
            fields=[
                ('inputoutput_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='web.inputoutput')),
                ('value', models.IntegerField(default=0, verbose_name='value')),
            ],
            options={
                'verbose_name': 'AI',
                'verbose_name_plural': 'AI',
            },
            bases=('web.inputoutput',),
        ),
        migrations.CreateModel(
            name='BinaryInput',
            fields=[
                ('inputoutput_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='web.inputoutput')),
                ('value', models.BooleanField(verbose_name='value')),
            ],
            options={
                'verbose_name': 'BI',
                'verbose_name_plural': 'BI',
            },
            bases=('web.inputoutput',),
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('register', models.IntegerField(verbose_name='register')),
                ('can_read', models.BooleanField(default=False, verbose_name='can_read')),
                ('can_write', models.BooleanField(default=False, verbose_name='can_write')),
                ('com_server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.comserver', verbose_name='comserver')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.employee', verbose_name='employee')),
            ],
            options={
                'verbose_name': 'Permission',
                'verbose_name_plural': 'Permissions',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='title')),
                ('register', models.IntegerField(default=0, verbose_name='register')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('status', models.CharField(choices=[('ENABLE', 'ENABLE'), ('DISABLE', 'DISABLE'), ('TOGGLE', 'TOGGLE'), ('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE'), ('POWER_ON', 'POWER_ON'), ('POWER_OFF', 'POWER_OFF'), ('START', 'START'), ('STOP', 'STOP'), ('INSTALLED', 'INSTALLED'), ('REMOVED', 'REMOVED'), ('unable to connect !', 'unable to connect !')], max_length=50, verbose_name='status')),
                ('description', models.CharField(blank=True, max_length=5000, null=True, verbose_name='description')),
                ('com_server', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.comserver', verbose_name='com_server')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.employee', verbose_name='employee')),
            ],
            options={
                'verbose_name': 'Log',
                'verbose_name_plural': 'Logs',
            },
        ),
        migrations.CreateModel(
            name='Feeder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('address', models.IntegerField(default=0, verbose_name='address')),
                ('register_cb_open', models.IntegerField(default=3, verbose_name='register_cb_open')),
                ('register_cb_close', models.IntegerField(default=4, verbose_name='register_cb_close')),
                ('register_cb_test', models.IntegerField(default=1, verbose_name='register_cb_test')),
                ('register_cb_trip', models.IntegerField(default=2, verbose_name='register_cb_trip')),
                ('register_cb_spare1', models.IntegerField(default=5, verbose_name='register_cb_spare1')),
                ('register_cb_spare2', models.IntegerField(default=6, verbose_name='register_cb_spare2')),
                ('register_ct_i_a', models.IntegerField(default=7, verbose_name='register I a')),
                ('register_ct_i_b', models.IntegerField(default=8, verbose_name='register I b')),
                ('register_ct_i_c', models.IntegerField(default=9, verbose_name='register I c')),
                ('register_vt_v_a', models.IntegerField(default=10, verbose_name='register V a')),
                ('register_vt_v_b', models.IntegerField(default=11, verbose_name='register V b')),
                ('register_vt_v_c', models.IntegerField(default=12, verbose_name='register V c')),
                ('register_vt_v_ab', models.IntegerField(default=13, verbose_name='register V ab')),
                ('register_vt_v_bc', models.IntegerField(default=14, verbose_name='register V bc')),
                ('register_vt_v_ac', models.IntegerField(default=15, verbose_name='register V ac')),
                ('register_q', models.IntegerField(default=16, verbose_name='register q')),
                ('register_p', models.IntegerField(default=17, verbose_name='register p')),
                ('register_s', models.IntegerField(default=18, verbose_name='register s')),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.bus', verbose_name='bus')),
                ('com_server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.comserver', verbose_name='com_server')),
            ],
            options={
                'verbose_name': 'Feeder',
                'verbose_name_plural': 'Feeders',
            },
        ),
        migrations.CreateModel(
            name='BinaryOutput',
            fields=[
                ('inputoutput_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='web.inputoutput')),
                ('value', models.BooleanField(verbose_name='value')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.employee', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'BinaryCommand',
                'verbose_name_plural': 'BinaryCommands',
            },
            bases=('web.inputoutput',),
        ),
    ]
