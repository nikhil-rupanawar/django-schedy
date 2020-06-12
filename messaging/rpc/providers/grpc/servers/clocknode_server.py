import os
import sys
import logging
import grpc
import pprint
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

    def __init__(self, server_conf):
        ClockNodeServiceServicer.__init__(self)
        ClockNodeContract.__init__(self)
        BaseRpcServerMixin.__init__(self)
        self._server_conf = server_conf
        self._registry_service_stub = RegistryServiceStub(self.server_conf.registry_service_uri)

    @property
    def registry_service_stub(self):
        return self._registry_service_stub

    @property
    def server_conf(self):
        return self._server_conf
    
    def _init_ticker(self):
        self._ticker = Ticker(
            self.server_conf.ticker_type,
            self.server_conf.ticker_config
        )

    def _start_ticker(self):
        self._ticker.start()

    def _stop_ticker(self):
        self._ticker.shutdown(wait=False)

    def start(self):
        print(f"Starting clock node with following configuration")
        pprint.pprint(self.server_conf)
        print("Registering to schedule director..")
        self._register_to_director()
        print("Starting to tick..")
        self._init_ticker()
        self._start_ticker()
        print("ACK_READY")
        self.ack_ready()

        print("\n\n====== Wating for first request.. =======")

        self._start_and_block()

    def ack_ready(self):
        pass

    def _register_to_director(self):
        self.registry_service_stub.register_clocknode(
            messages.M_RegisterClockNodeRequest(
                 messages.M_ClockNode(
                    self.server_conf.uuid,
                    self.server_conf.uri,
                    self.server_conf.minute,
                    self.server_conf.max_schedule_count,
                 ),
                 reschedule_on_registration=True,
             )
        )

    def _start_and_block(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_ClockNodeServiceServicer_to_server(self, server)
        server.add_insecure_port(f'{self.server_conf.server_network_interface}:{self.server_conf.server_network_port}')
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
        pass

    def remove_schedule(self, request, context):
        self.ticker.remove_job(request.id)

    def _add_job(self, schedule_details):
        print("Triggered {schedule_details}")

    def health_ping(self, request, context):
        return HealthPingResponse()


if __name__ == '__main__':
    service = ClockNodeService()
    service.start()
