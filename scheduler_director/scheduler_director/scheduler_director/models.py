import os
import enum
from uuid import uuid4
from django.db import models

# Create your models here.
from django.db import models


class Director(models.Model):
    uuid = models.UUIDField(default=uuid4)
    name = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    registery_service_uri = models.CharField(max_length=255)
    clocknode_event_service_uri = models.CharField(max_length=255)
    schedule_event_service_uri = models.CharField(max_length=255)
    minute_space_size = models.IntegerField()

    def register_clock_node(self, clocknode):
        return clocknode.save()

    def deregister_clock_node(self, clocknode):
        clocknode.deregister()

    def route(self, schedule):
        ...

    def rebalance(self, clocknodes):
        ...

    def configure(self, config):
        ...

    @classmethod
    def initialize(cls):
        if cls.objects.first():
            return

        cls.objects.create(
            name='test',
            registery_service_uri=os.environ.get(
                'SCHEDULER_DIRECTOR_REGISTERY_SERVICE_URI',
                'grpc://localhost:50000'
            ),
            clocknode_event_service_uri=os.environ.get(
                'SCHEDULER_DIRECTOR_CLOCKNODE_EVENT_SERVICE_URI',
                'grpc://localhost:50001'
            ),
            schedule_event_service_uri=os.environ.get(
                'SCHEDULE_TARGET_URI',
                'amqp://guest@localhost:5672/default_schedule_target_topic'
            ),
            minute_space_size=int(os.environ.get('MINUTE_SPACE_SIZE', 1)),
       )


class ClockNode(models.Model):
    uri = models.CharField(max_length=255)
    last_seen = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_used = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    schedule_count = models.IntegerField(null=True)
    max_schedule_count = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    registered_on = models.DateTimeField(auto_now_add=True)
    reschdule_on_registration = models.BooleanField(default=True)
    is_disabled = models.BooleanField(null=True)
    is_deleted = models.BooleanField(null=True)
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True)

    @classmethod
    def select_node(cls, schedule):
        raise NotImplementedError("Not implemented")

    def route(self, schedule):
        raise NotImplementedError("Not implemented")

    @property
    def rpcclient(self):
        return rpc.rpcclient.ClockNodeRpcClient(self.uri)

    def deregister():
        try:
            self.rpcclient.deregister()
        except rpcclient.ClockNodeRpcClient.ConnectionError:
            logger.warning('Failed to communicate with clocknode {self}.')
        self.is_disabled = self.is_deleted = True
        self.save()


class MinuteHandClockNode(ClockNode):
    minute = models.IntegerField()

    @classmethod
    def select_node(cls, schedule):
        ...

    @classmethod
    def from_registration_request(cls, registration_request):
        if registration_request.body.minute == 0:
            hour = 0
        else:
            hour = registration_request.body.minute / 60
        return cls(
            minute_id=registration_request.body.minute + 1,
            minute=registration_request.body.minute,
            hour=hour,
            hour_id=hour + 1,
        )


    def route(self, schedule):
        ...

    def ping(self):
        ...


class Schedule(models.Model):
    class TriggerType(models.TextChoices):
        CRON = "CRON"

    class Type(enum.IntEnum):
        MINUTELY = 1
        HOURLY = 2
        DAILY = 3
        WEEKLY = 4
        MONTHLY = 5
        YEARLY = 6
        ONCE = 7

    name = models.CharField(max_length=500)
    description = models.TextField()
    trigger_type = models.CharField(
        max_length=50,
        choices=TriggerType.choices,
        default=TriggerType.CRON,
    )
    create = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    create_by = models.CharField(max_length=255)
    clocknode = models.ForeignKey(ClockNode, on_delete=models.SET_NULL, null=True)
    misfire_grace_time = models.IntegerField(null=True)
    type = models.IntegerField(null=True)


class CronSchedule(Schedule):
    second = models.CharField(max_length=255, null=True)
    minute = models.CharField(max_length=255, null=True)
    hour = models.CharField(max_length=255, null=True)
    day = models.CharField(max_length=255, null=True)
    day_of_week = models.CharField(max_length=255, null=True)
    week = models.CharField(max_length=255, null=True)
    month = models.CharField(max_length=255, null=True)
    year = models.CharField(max_length=255, null=True)
    start_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    end_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    timezone = models.CharField(max_length=255, null=True)
    jitter = models.IntegerField(null=True)

    def to_dict(self):
        d = self.__dict__.copy()

