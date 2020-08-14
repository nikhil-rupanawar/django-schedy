import os
import enum
import datetime
import copy
import django.db.models.options as options
from uuid import uuid4, UUID
from django.db import models
from django_model_to_dict.mixins import ToDictMixin
from common.util import DictModel
from django.db import models

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('to_message_fields',)

# Create your models here.

def now():
    return datetime.datetime.utcnow()


class ToMessageMixin(ToDictMixin):
    def to_message(self):
        to_message_fields = getattr(self._meta, 'to_message_fields', set([]))
        to_message_fields_exclude = getattr(self._meta, 'to_message_fields_exclude', set([]))
        value_dict = deepcopy(self.__dict__)
        msg = DictModel()
        for k, v in value_dict.items():
            if k not in to_message_fields or k in to_message_fields_exclude:
                continue
            elif isinstance(v, (datetime.datetime, UUID)):
                msg[k] = str(v)
            else:
                msg[k] = v
        return msg


class Director(models.Model):
    uuid = models.UUIDField(default=uuid4)
    name = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    registery_service_uri = models.CharField(max_length=255)
    clocknode_event_service_uri = models.CharField(max_length=255)
    schedule_event_service_uri = models.CharField(max_length=255)
    minute_space_size = models.IntegerField(null=True)
    is_space_size_dynamic = models.BooleanField(default=True)

    @classmethod
    def select(cls):
        return cls.objects.first()

    @classmethod
    def register_clocknode(cls, request):
        try:
            clocknode = MinuteHandClockNode.objects.get(uuid=request.node.uuid)
            clocknode.update_from_registration_request(request)
            clocknode.save()
            return clocknode
        except ClockNode.DoesNotExist:
            clocknode = MinuteHandClockNode.from_registration_request(request)
            clocknode.director = cls.select()
            clocknode.save()
            return clocknode

    def unregister_clocknode(self, request):
        ...

    def route(self, schedule):
        ...

    def rebalance(self, clocknodes):
        ...

    def configure(self, config):
        ...

    @classmethod
    def initialize(cls):
        if cls.select():
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

    def get_minute_space_size(self):
        if self.is_space_size_dynamic:
            return MinuteHandClockNode.objects.distinct('minute').count()
        return self.minute_space_size

    def select_clocknodes_by_minute_hand(self, schedule):
        minute_space_size = self.get_minute_space_size()
        if not minute_space_size:
            raise Exception('No ClockNode is registered to director')
        schedule_minute = schedule.minute
        schedule_hour = schedule.hour
        if '/' in minute:
            minute = minute.split('/')[1]
        minute = int(minute)
        minute_bucket = ((schedule_hour * 60) + schedule_minute) % self.get_minute_space_size()
        return self.minutehandclocknode_set.order_by('last_used').filter(minute=minute_bucket)


class AbstractClockNode(models.Model):

    class Type(models.TextChoices):
        MINUTE_HAND = "MINUTE_HAND"

    class Meta:
        abstract = True

    uuid = models.UUIDField(unique=True)
    uri = models.CharField(max_length=255)
    schedule_count = models.IntegerField(null=True)
    max_schedule_count = models.IntegerField(null=True)
    reschdule_on_registration = models.BooleanField(default=True)
    is_disabled = models.BooleanField(null=True, default=False)
    is_deleted = models.BooleanField(null=True, default=False)
    last_seen = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_used = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    registered_on = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)


    @property
    def rpcclient(self):
        return rpc.rpcclient.ClockNodeRpcClient(self.uri)

    def unregister():
        try:
            self.rpcclient.deregister()
        except rpcclient.ClockNodeRpcClient.ConnectionError:
            logger.warning('Failed to communicate with clocknode {self}.')
        self.is_disabled = self.is_deleted = True
        self.save()

    def update_from_registration_request(self, request):
        self.uri = request.node.uri 
        self.max_schedule_count = request.node.max_schedule_count
        self.last_seen = now()
        self.reschedule_on_registration = request.reschedule_on_registration

    @classmethod
    def from_registration_request(cls, request):
        # TODO: support mutltiple algos and types
        return MinuteHandClockNode.from_registration_request(request)


class MinuteHandClockNode(AbstractClockNode):
    minute = models.IntegerField()
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True)

    @classmethod
    def from_registration_request(cls, request):
        clocknode = cls(
            uuid=request.node.uuid,
            minute=request.node.minute or 0 # TODO remove -- only for testing
        )
        clocknode.update_from_registration_request(request)
        return clocknode

    def route(self, schedule):
        ...

    def ping(self):
        ...


class AbstractSchedule(models.Model):

    class Meta:
        abstract = True

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
    misfire_grace_time = models.IntegerField(null=True)
    type = models.IntegerField(null=True)


class CronSchedule(AbstractSchedule):
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
    clocknode = models.ForeignKey(MinuteHandClockNode, on_delete=models.SET_NULL, null=True)

