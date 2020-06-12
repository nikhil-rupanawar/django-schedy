import functools
from messaging.messages import BaseMessage
from messaging.rpc.providers.grpc.util import protobuf_to_dict, dict_to_protobuf

def marshal(request_msg_cls, response_proto_cls):
    def wrapper(f):
        @functools.wraps(f)
        def wrapped(self, request_proto_incoming, context):
            try:
                request_msg = protobuf_to_dict(request_proto_incoming, cls=request_msg_cls)
                response = f(self, request_msg, context)
                if isinstance(response, BaseMessage):
                    return dict_to_protobuf(response_proto_cls, response)
            except:
                import traceback
                traceback.print_exc()
        return wrapped
    return wrapper

