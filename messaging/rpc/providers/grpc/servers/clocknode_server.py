import os
import sys
import logging
import grpc
from concurrent import futures
from functools import partial
from messaging.rpc.contracts import ClockNodeContract
from messaging.rpc.rpcserver import BaseRpcServerMixin
from messaging.rpc.providers.grpc.interfaces.messages_pb2 import (
    ReplaceSchedulesResponse,
    AddScheduleResponse,
    RemoveScheduleResponse,
    HealthPingResponse,
)
from messaging.rpc.providers.grpc.interfaces.clocknode_service_pb2_grpc import (
    ClockNodeServiceServicer,
    add_ClockNodeServiceServicer_to_server
)
from messaging.rpc.providers.grpc.interfaces.registry_service_pb2_grpc import RegistryServiceStub
from messaging.rpc.rpcclient import RegistryServiceStub
from messaging import messages
from common.tickers import Ticker


logger = logging.getLogger(__name__)


class ClockNodeServer(
        ClockNodeServiceServicer,
        ClockNodeContract,
        BaseRpcServerMixin,
    ):

    def __init__(self, server_config):
        ClockNodeServiceServicer.__init__(self)
        ClockNodeContract.__init__(self)
        BaseRpcServerMixin.__init__(self)
        self._server_config = server_config

    @property
    def server_config(self):
        return self._server_config
    
    def _init_ticker(self):
        self._ticker = Ticker(
            self.server_config.ticker_type,
            self.server_config.ticker_config
        )

    def _start_ticker(self):
        self._ticker.start()

    def _stop_ticker(self):
        self._ticker.shutdown(wait=False)

    def start(self):
        self.register_to_director()
        self._init_ticker()
        self._start_ticker()
        self.ack_ready()
        self._start_and_block()

    def ack_ready(self):
        pass

    def register_to_director(self):
        conf = self.server_config
        print(conf)
        registry_service_stub = RegistryServiceStub(conf.registry_service_uri)
        registry_service_stub.register_clocknode(
            messages.M_RegisterClockNodeRequest(
                 messages.M_ClockNode(
                    conf.uuid,
                    conf.uri,
                    conf.minute,
                    conf.max_schedule_count,
                 ),
                 reschedule_on_registration=True,
             )
        )

    def _start_and_block(self):
        config = self.server_config
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_ClockNodeServiceServicer_to_server(self, server)
        server.add_insecure_port(f'{config.server_network_interface}:{config.server_network_port}')
        server.start()
        server.wait_for_termination()

    def stop(self):
        self.stop_ticker()

    def replace_schedules(self, request, context):
        self.ticker.remove_all_jobs()
        for job_definition in request.sch:
            self._add_job(job_definition)
        return ReplaceSchedulesResponse()

    def add_schedule(self, request, context):
        logger.info('Adding job {}'.format(request.job_definition.id))
        self._schedule_job(request.job_definition)
        return AddScheduleResponse()

    def remove_schedule(self, request, context):
        self.ticker.remove_job(request.id)

    def _add_job(self, schedule_details):
        print("Triggered {schedule_details}")

    def health_ping(self, request, context):
        return HealthPingResponse()


if __name__ == '__main__':
    service = ClockNodeService()
    service.start()
