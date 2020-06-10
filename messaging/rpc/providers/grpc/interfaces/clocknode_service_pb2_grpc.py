# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import messaging.rpc.providers.grpc.interfaces.messages_pb2 as messages__pb2


class ClockNodeServiceStub(object):
    """Missing associated documentation comment in .proto file"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.add_schedule = channel.unary_unary(
                '/messaging.rpc.providers.grpc.proto.clocknode.ClockNodeService/add_schedule',
                request_serializer=messages__pb2.AddScheduleRequest.SerializeToString,
                response_deserializer=messages__pb2.AddScheduleResponse.FromString,
                )
        self.remove_schedule = channel.unary_unary(
                '/messaging.rpc.providers.grpc.proto.clocknode.ClockNodeService/remove_schedule',
                request_serializer=messages__pb2.RemoveScheduleRequest.SerializeToString,
                response_deserializer=messages__pb2.RemoveScheduleResponse.FromString,
                )
        self.replace_schedules = channel.unary_unary(
                '/messaging.rpc.providers.grpc.proto.clocknode.ClockNodeService/replace_schedules',
                request_serializer=messages__pb2.ReplaceSchedulesRequest.SerializeToString,
                response_deserializer=messages__pb2.ReplaceSchedulesResponse.FromString,
                )
        self.health_ping = channel.unary_unary(
                '/messaging.rpc.providers.grpc.proto.clocknode.ClockNodeService/health_ping',
                request_serializer=messages__pb2.HealthPingRequest.SerializeToString,
                response_deserializer=messages__pb2.HealthPingResponse.FromString,
                )


class ClockNodeServiceServicer(object):
    """Missing associated documentation comment in .proto file"""

    def add_schedule(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def remove_schedule(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def replace_schedules(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def health_ping(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ClockNodeServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'add_schedule': grpc.unary_unary_rpc_method_handler(
                    servicer.add_schedule,
                    request_deserializer=messages__pb2.AddScheduleRequest.FromString,
                    response_serializer=messages__pb2.AddScheduleResponse.SerializeToString,
            ),
            'remove_schedule': grpc.unary_unary_rpc_method_handler(
                    servicer.remove_schedule,
                    request_deserializer=messages__pb2.RemoveScheduleRequest.FromString,
                    response_serializer=messages__pb2.RemoveScheduleResponse.SerializeToString,
            ),
            'replace_schedules': grpc.unary_unary_rpc_method_handler(
                    servicer.replace_schedules,
                    request_deserializer=messages__pb2.ReplaceSchedulesRequest.FromString,
                    response_serializer=messages__pb2.ReplaceSchedulesResponse.SerializeToString,
            ),
            'health_ping': grpc.unary_unary_rpc_method_handler(
                    servicer.health_ping,
                    request_deserializer=messages__pb2.HealthPingRequest.FromString,
                    response_serializer=messages__pb2.HealthPingResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'messaging.rpc.providers.grpc.proto.clocknode.ClockNodeService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ClockNodeService(object):
    """Missing associated documentation comment in .proto file"""

    @staticmethod
    def add_schedule(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/messaging.rpc.providers.grpc.proto.clocknode.ClockNodeService/add_schedule',
            messages__pb2.AddScheduleRequest.SerializeToString,
            messages__pb2.AddScheduleResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def remove_schedule(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/messaging.rpc.providers.grpc.proto.clocknode.ClockNodeService/remove_schedule',
            messages__pb2.RemoveScheduleRequest.SerializeToString,
            messages__pb2.RemoveScheduleResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def replace_schedules(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/messaging.rpc.providers.grpc.proto.clocknode.ClockNodeService/replace_schedules',
            messages__pb2.ReplaceSchedulesRequest.SerializeToString,
            messages__pb2.ReplaceSchedulesResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def health_ping(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/messaging.rpc.providers.grpc.proto.clocknode.ClockNodeService/health_ping',
            messages__pb2.HealthPingRequest.SerializeToString,
            messages__pb2.HealthPingResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
