import urllib
import grpc
import functools
from messaging.rpc.providers.grpc.util import dict_to_protobuf, protobuf_to_dict

class BaseStubProxy:
    def __init__(self, uri):
        self._uriparsed = urllib.parse.urlparse(uri)
        self._channel = grpc.insecure_channel(self._uriparsed.netloc)
        self._stub = self.grpc_stub_cls(self._channel)

    @classmethod
    def marshal(cls, request_proto_cls, response_msg_cls):
        def wrapper(f):
            @functools.wraps(f)
            def wrapped(self, msg):
                request_proto = dict_to_protobuf(request_proto_cls, msg)
                response_proto = response_msg = f(self, request_proto)
                if response_msg_cls:
                    response_msg = protobuf_to_dict(response_proto, cls=response_msg_cls)
                return response_msg
            return wrapped
        return wrapper


marshal = BaseStubProxy.marshal

