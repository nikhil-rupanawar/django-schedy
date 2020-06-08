import urllib


class ClockNodeRpcClient:
    """ Mixin for clock node rpc clients """

    def __init__(self, uri):
        return self._get_client(uri)

    def add_schedule(self, request):
        raise NotImplementedError()

    def remove_schedule(self, request):
        raise NotImplementedError()

    def replace_schedules(self, request):
        raise NotImplementedError()

    def health_ping(self, request):
        raise NotImplementedError()

    @classmethod
    def _get_client(cls, uri):
        uriparsed = urllib.parse.urlparse(uri)
        from messaging.rpc.providers.grpc.clients import ClockNodeGrpcClient
        if uriparsed.startswith('grpc://'):
            return GrpcClockNodeClient(uri)
        else:
            raise Exception('RPC provider for scheme {uriparsed.scheme} is not supported.')

