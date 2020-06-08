from django.core.management.base import BaseCommand
# TODO Strategy Pattern
from messaging.rpc.providers.grpc.servers.clocknode_server import ClockNodeServer

class Command(BaseCommand):
    help = 'ClockNode service'

    def add_arguments(self, parser):
        pass
        #parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        service = ClockNodeServer()
        service.start()
