from uuid import uuid4
from django.db import models

# Create your models here.
from django.db import models


class SchedulerDirector(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid4)
    hostname = models.CharField(max_length=255)
    cluster_uuid = models.UUIDField(default=uuid4)
    cluster_name = models.CharField(max_length=500)


class ClockNode(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid4)
    hostname = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True)
    last_heatbeat = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    disabled = models.BooleanField(default=False)
