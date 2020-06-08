from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

# TODO Strategy Pattern
from messaging.rpc.providers.grpc.servers.registry_server import RegistryServer


class Command(BaseCommand):
    help = 'Schdule director registry service'

    def add_arguments(self, parser):
        pass
        #parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        service = RegistryServer()
        service.start()
