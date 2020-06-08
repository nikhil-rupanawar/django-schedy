import os
import sys
import logging
import grpc
import django
from django.conf import settings
from concurrent import futures
from functools import partial
from messaging.rpc.providers.grpc.interfaces.messages_pb2 import (
    RegisterClockNodeResponse
)
from messaging.rpc.providers.grpc.interfaces.registry_service_pb2_grpc import RegistryServiceServicer, add_RegistryServiceServicer_to_server

from scheduler_director.scheduler_director import models


logger = logging.getLogger(__name__)


class RegistryServer(RegistryServiceServicer):

    @property
    def server_config(self):
        return {
            'port': os.environ.get('PORT', 50001),
            'network_interface': os.environ.get('NETWORK_INTERFACE', '[::]')
        }


    def start(self):
        self._start_and_block()

    def _start_and_block(self):
        config = self.server_config
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_RegistryServiceServicer_to_server(self, server)
        server.add_insecure_port(f'{config["network_interface"]}:{int(config["port"])}')
        server.start()
        server.wait_for_termination()

    def stop(self):
        pass

    def register_clock_node(self, request, context):
        print("here")
        return RegisterClockNodeResponse()


if __name__ == '__main__':
    service = RegistryService()
    service.start()
