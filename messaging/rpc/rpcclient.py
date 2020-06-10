import urllib
import abc
from .contracts import ClockNodeContract, RegistryServiceContract


def ClockNodeStub(uri):
    if uri.startswith('grpc://'):
        from messaging.rpc.providers.grpc.clients.clocknode import ClockNodeStubProxy
        return ClockNodeStubProxy(uri)
    else:
        raise Exception('Provider for scheme {uriparsed.scheme} is not supported.')


def RegistryServiceStub(uri):
    if uri.startswith('grpc://'):
        from messaging.rpc.providers.grpc.clients.registry_service import RegistryServiceStubProxy
        return RegistryServiceStubProxy(uri)
    else:
        raise Exception('Provider for scheme {uriparsed.scheme} is not supported.')
