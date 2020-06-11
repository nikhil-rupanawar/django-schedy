import os
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler


class BaseRpcServerMixin:

    @property
    def server_config(self):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError()

    def init(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass


def ClockNodeRpcServer(server_config):
    if server_config.uri.startswith('grpc://'):
        from messaging.rpc.providers.grpc.servers.clocknode_server import ClockNodeServer
        return ClockNodeServer(server_config)

def RegistryServiceServer(server_config):
    if server_config.uri.startswith('grpc://'):
        from messaging.rpc.providers.grpc.servers.registry_service import RegistryServiceServer
        return RegistryServiceServer(service_config)


