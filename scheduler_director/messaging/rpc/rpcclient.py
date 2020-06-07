import urllib

class ClockNodeRpcClient:
    def __init__(self, uri):
        return ClockNodeRpcClientFactory.get_client(uri)

    def add_schedule(self, add_schedule_request):
        raise NotImplementedError()

    def remove_schedule(self, remove_schedule_request):
        raise NotImplementedError()

    def heartbeat(self):
        raise NotImplementedError()

    def stats(self, stats_request):
        raise NotImplementedError()


class ClockNodeRpcClientFactory:
    @classmethod
    def get_client(cls, uri):
        uriparsed = urllib.parse.urlparse(uri)
        from messaging.rpc.providers.grpc import ClockNodeGrpcClient
        if uriparsed.startswith('grpc://'):
            return GrpcClockNodeClient(uri)
        else:
            raise Exception('RPC provider for scheme {uriparsed.scheme} is not supported.')

