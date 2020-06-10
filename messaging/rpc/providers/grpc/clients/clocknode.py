import grpc
from messaging.rpc.contracts import ClockNodeContract
from messaging.rpc.provider.grpc.interfaces.clocknode_service_pb2_grpc import ClockNodeServiceStub
from messaging.rpc.provider.grpc.interfaces.messages_pb2 import (
    AddScheduleRequest,
    RemoveScheduleRequest,
    ReplaceScheduleRequest,
    HealthPingRequest,
)
from .base import BaseStubProxy, marshal


class ClockNodeStubProxy(BaseStubProxy, ClockNodeContract):
    """ GRPC clock node service clients """

    grpc_stub_cls = ClockNodeServiceStub

    def __init__(self, uri):
        super().__init__(uri)

    @marshal(AddScheduleRequest)
    def add_schedule(self, msg):
        return self._stub.add_schedule(msg)

    @marshal(RemoveScheduleRequest)
    def remove_schedule(self, msg):
        return self._stub.remove_schedule(msg)

    @marshal(ReplaceScheduleRequest)
    def replace_schedules(self, msg):
        return self._stub.replace_schedule(msg)

    @marshal(HealthPingRequest)
    def health_ping(self, msg):
        return self._stub.health_ping(msg)
