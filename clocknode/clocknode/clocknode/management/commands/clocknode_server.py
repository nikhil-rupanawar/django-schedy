import os
from django.core.management.base import BaseCommand
# TODO Strategy Pattern
from messaging.rpc.providers.grpc.servers.clocknode_server import ClockNodeServer
from messaging.rpc.server_configs import ClockNodeServerConfig


class Command(BaseCommand):
    help = 'ClockNode server instance'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        clocknode_server_config = ClockNodeServerConfig.from_env()
        service = ClockNodeServer(clocknode_server_config)
        service.start()
