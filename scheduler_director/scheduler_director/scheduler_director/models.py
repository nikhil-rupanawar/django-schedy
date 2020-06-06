import enum
from uuid import uuid4
from django.db import models

# Create your models here.
from django.db import models


class Director(models.Model):
    class PartitionStrategy(enum.Enum):
        ROUND_ROBIN = "ROUND_ROBIN"
        MINUTE_HAND = "MINUTE_HAND"
        HOUR_HAND = "HOUR_HAND"

    DEHAULT_PARTITION_STRATEGY = "ROUND_ROBIN"

    uuid = models.UUIDField(default=uuid4)
    name = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    registery_service_uri = models.CharField(max_length=255)

    def register_clock_node(self, clocknode):
        return clocknode.save()

    def deregister_clock_node(self, clocknode):
        return clocknode.delete()

    def route(self, schedule):
        ...

    def rebalance(self, clocknodes):
        ...

    def ping(self, clocknode):
        ...


class ClockNode(models.Model):
    uri = models.CharField(max_length=255)
    last_seen = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_used = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    disabled = models.BooleanField(default=False)
    schedule_count = models.IntegerField(null=True)
    max_schedule_count = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    registered_on = models.DateTimeField(auto_now_add=True)
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True)

    @classmethod
    def select_node(cls, schedule):
        raise NotImplementedError("Not implemented")

    def route(self, schedule):
        raise NotImplementedError("Not implemented")

    @property
    def rpc(self):
        return rpcclient.RPCClient(self.uri)


class RoundRobinClockNode(ClockNode):
    class Meta:
        proxy = True

    @classmethod
    def select_node(cls, schedule):
        ...

    def route(self, schedule):
        ...

    def ping(self):
        ...


class MinuteHandClockNode(ClockNode):
    minute = models.IntegerField()
    minute_id = models.IntegerField()
    hour = models.IntegerField()
    hour_id = models.IntegerField()

    @classmethod
    def select_node(cls, schedule):
        ...

    @classmethod
    def populate(cls, director):
        for minute in range(0, 1439):
            if minute == 0:
                hour = 0
            else:
                hour = minute / 60

            cls.objects.create(
                minute_id=minute + 1,
                minute=minute,
                director=director,
                hour=hour,
                hour_id=hour + 1,
            )

    def un_register(self):
        self.rpc.disable()
        self.delete()

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

    def un_register(self):
        self.rpc.disable()

    def route(self, schedule):
        ...

    def ping(self):
        ...


class HourHandClockNode(ClockNode):
    hour = models.IntegerField()
    hour_id = models.IntegerField()

    @classmethod
    def select_node(cls, schedule):
        ...

    def route(self, schedule):
        ...

    def ping(self):
        ...


class Schedule(models.Model):
    class TriggerType(models.TextChoices):
        CRON = "CRON"

    name = models.CharField(max_length=500)
    description = models.TextField()
    trigger_type = models.CharField(
        max_length=50, choices=TriggerType.choices, default=TriggerType.CRON,
    )
    create = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    create_by = models.CharField(max_length=255)
    clocknode = models.ForeignKey(ClockNode, on_delete=models.SET_NULL, null=True)


class CronSchedule(Schedule):
    class Type(enum.IntEnum):
        MINUTELY = 1
        HOURLY = 2
        DAILY = 3
        WEEKLY = 4
        MONTHLY = 5
        YEARLY = 6
        ONCE = 7

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
    type = models.IntegerField(null=True)
