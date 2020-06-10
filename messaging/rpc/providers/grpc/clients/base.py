import urllib
import grpc
import functools
from messaging.rpc.providers.grpc.util import dict_to_protobuf


class BaseStubProxy:
    def __init__(self, uri):
        self._uriparsed = urllib.parse.urlparse(uri)
        self._channel = grpc.insecure_channel(self._uriparsed.netloc)
        self._stub = self.grpc_stub_cls(self._channel)

    @classmethod
    def marshal(cls, request_cls, response_cls=None):
        def wrapper(f):
            @functools.wraps(f)
            def wrapped(self, msg):
                request_proto = dict_to_protobuf(msg, request_cls)
                response = f(self, request_proto)
                #if response_cls:
                #    response_msg = protobuf_to_msg(response)
                return response
            return wrapped
        return wrapper


marshal = BaseStubProxy.marshal

