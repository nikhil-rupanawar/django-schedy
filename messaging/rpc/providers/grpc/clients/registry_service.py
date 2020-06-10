import grpc
from messaging.rpc.contracts import RegistryServiceContract
from messaging.rpc.providers.grpc.interfaces.registry_service_pb2_grpc import RegistryServiceStub
from messaging.rpc.providers.grpc.interfaces.messages_pb2 import (
    RegisterClockNodeRequest,
)
from .base import BaseStubProxy, marshal


class RegistryServiceStubProxy(BaseStubProxy, RegistryServiceContract):
    """ GRPC clock node service clients """

    grpc_stub_cls = RegistryServiceStub

    def __init__(self, uri):
        super().__init__(uri)

    @marshal(RegisterClockNodeRequest)
    def register_clocknode(self, msg):
        print(msg, "****")
        return self._stub.register_clock_node(msg)

