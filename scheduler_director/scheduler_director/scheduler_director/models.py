import os
import enum
import datetime
from uuid import uuid4, UUID
from django.db import models
from django_model_to_dict.mixins import ToDictMixin
from common.util import DictModel

# Create your models here.
from django.db import models


def now():
    return datetime.datetime.utcnow()


class ToMessageMixin(ToDictMixin):
    to_message_fields = set()
    to_message_fields_exclude = set()

    def to_message(self):
        value_dict = DictModel(**super().to_dict())
        msg = {}
        for k, v in value_dict.items():
            if self.to_message_fields != '*' and (k not in self.to_message_fields or k in to_message_fields_exclude):
                continue
            elif isinstance(v, (datetime.datetime, UUID)):
                msg[k] = str(v)
            else:
                msg[k] = v
        return msg


class Director(models.Model, ToMessageMixin):
    uuid = models.UUIDField(default=uuid4)
    name = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    registery_service_uri = models.CharField(max_length=255)
    clocknode_event_service_uri = models.CharField(max_length=255)
    schedule_event_service_uri = models.CharField(max_length=255)
    minute_space_size = models.IntegerField()
 
    # Move to meta
    to_message_fields = {'uuid', 'registery_service_uri', 'schedule_event_service_uri'}

    @classmethod
    def register_clocknode(cls, request):
        print(request.reschedule_on_registration, "hjhjh")
        print(request.node.max_schedule_count, "hjhjh")
        print(type(request.node.max_schedule_count), "hjhjh")
        try:
            clocknode = ClockNode.objects.get(uuid=request.node.uuid)
            clocknode.update_from_registration_request(request)
            clocknode.save()
            return clocknode
        except ClockNode.DoesNotExist:
            clocknode = ClockNode.from_registration_request(request)
            clocknode.director = cls.objects.first()
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


class ClockNode(models.Model, ToMessageMixin):
    class Type(models.TextChoices):
        MINUTE_HAND = "MINUTE_HAND"

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
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True)

    @classmethod
    def select_node(cls, schedule):
        raise NotImplementedError("Not implemented")

    def route(self, schedule):
        raise NotImplementedError("Not implemented")

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


class MinuteHandClockNode(ClockNode):
    minute = models.IntegerField()

    @classmethod
    def select_node(cls, schedule):
        ...

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


class Schedule(models.Model, ToMessageMixin):
    to_message_exclude_fields = {'created', 'updated', 'clocknode'}

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

    def to_message(self):
        return DictModel(self.to_dict())

