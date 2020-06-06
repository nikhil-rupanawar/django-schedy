# Generated by Django 3.0.7 on 2020-06-06 08:48

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClockNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uri', models.CharField(max_length=255)),
                ('last_seen', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_used', models.DateTimeField(auto_now_add=True, null=True)),
                ('disabled', models.BooleanField(default=False)),
                ('schedule_count', models.IntegerField(null=True)),
                ('max_schedule_count', models.IntegerField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('registered_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('name', models.CharField(max_length=500)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('registery_service_uri', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField()),
                ('trigger_type', models.CharField(choices=[('CRON', 'Cron')], default='CRON', max_length=50)),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('create_by', models.CharField(max_length=255)),
                ('clocknode', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='scheduler_director.ClockNode')),
            ],
        ),
        migrations.CreateModel(
            name='CronSchedule',
            fields=[
                ('schedule_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='scheduler_director.Schedule')),
                ('second', models.CharField(max_length=255, null=True)),
                ('minute', models.CharField(max_length=255, null=True)),
                ('hour', models.CharField(max_length=255, null=True)),
                ('day', models.CharField(max_length=255, null=True)),
                ('day_of_week', models.CharField(max_length=255, null=True)),
                ('week', models.CharField(max_length=255, null=True)),
                ('month', models.CharField(max_length=255, null=True)),
                ('year', models.CharField(max_length=255, null=True)),
                ('start_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('end_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('timezone', models.CharField(max_length=255, null=True)),
                ('jitter', models.IntegerField(null=True)),
                ('type', models.IntegerField(null=True)),
            ],
            bases=('scheduler_director.schedule',),
        ),
        migrations.CreateModel(
            name='HourHandClockNode',
            fields=[
                ('clocknode_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='scheduler_director.ClockNode')),
                ('hour', models.IntegerField()),
                ('hour_id', models.IntegerField()),
            ],
            bases=('scheduler_director.clocknode',),
        ),
        migrations.CreateModel(
            name='MinuteHandClockNode',
            fields=[
                ('clocknode_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='scheduler_director.ClockNode')),
                ('minute', models.IntegerField()),
                ('minute_id', models.IntegerField()),
                ('hour', models.IntegerField()),
                ('hour_id', models.IntegerField()),
            ],
            bases=('scheduler_director.clocknode',),
        ),
        migrations.AddField(
            model_name='clocknode',
            name='director',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='scheduler_director.Director'),
        ),
        migrations.CreateModel(
            name='RoundRobinClockNode',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('scheduler_director.clocknode',),
        ),
    ]