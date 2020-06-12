import os
import sys
import logging
import grpc
import django
from django.conf import settings
from concurrent import futures
from functools import partial

from messaging.rpc.contracts import RegistryServiceContract
from messaging.rpc.rpcserver import BaseRpcServerMixin
from messaging.rpc.providers.grpc.util import protobuf_to_dict
from messaging.rpc.providers.grpc.interfaces.messages_pb2 import (
    RegisterClockNodeRequest,
    RegisterClockNodeResponse,
)
from messaging.messages import (
    M_RegisterClockNodeRequest,
    M_RegisterClockNodeResponse
)
from messaging.rpc.providers.grpc.interfaces.registry_service_pb2_grpc import (
    RegistryServiceServicer,
    add_RegistryServiceServicer_to_server
)
from scheduler_director.scheduler_director import models
from .base import marshal

logger = logging.getLogger(__name__)


class RegistryServer(
        RegistryServiceServicer,
        RegistryServiceContract,
        BaseRpcServerMixin,
    ):

    def __init__(self, server_config):
        RegistryServiceServicer.__init__(self)
        RegistryServiceContract.__init__(self)
        BaseRpcServerMixin.__init__(self)
        self._server_config = server_config

    @property
    def server_config(self):
        return self._server_config

    def start(self):
        self._start_and_block()

    def _start_and_block(self):
        config = self.server_config
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_RegistryServiceServicer_to_server(self, server)
        server.add_insecure_port(f'{config.server_network_interface}:{config.server_network_port}')
        server.start()
        server.wait_for_termination()

    def stop(self):
        pass

    def register_clocknode(self, request, context):
        print(request)

    # TODO because typo two method. it should be register_clocknode
    @marshal(M_RegisterClockNodeRequest, RegisterClockNodeResponse)
    def register_clock_node(self, request, context):
        self.register_clocknode(request, context)
        return M_RegisterClockNodeResponse()

if __name__ == '__main__':
    service = RegistryService()
    service.start()
