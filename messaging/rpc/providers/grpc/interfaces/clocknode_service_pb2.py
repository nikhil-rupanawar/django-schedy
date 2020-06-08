# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: clocknode_service.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import messages_pb2 as messages__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='clocknode_service.proto',
  package='messaging.rpc.providers.grpc.proto.clocknode',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x17\x63locknode_service.proto\x12,messaging.rpc.providers.grpc.proto.clocknode\x1a\x0emessages.proto2\xad\x04\n\x10\x43lockNodeService\x12\x7f\n\x0c\x61\x64\x64_schedule\x12\x36.messaging.rpc.providers.grpc.proto.AddScheduleRequest\x1a\x37.messaging.rpc.providers.grpc.proto.AddScheduleResponse\x12\x88\x01\n\x0fremove_schedule\x12\x39.messaging.rpc.providers.grpc.proto.RemoveScheduleRequest\x1a:.messaging.rpc.providers.grpc.proto.RemoveScheduleResponse\x12\x8e\x01\n\x11replace_schedules\x12;.messaging.rpc.providers.grpc.proto.ReplaceSchedulesRequest\x1a<.messaging.rpc.providers.grpc.proto.ReplaceSchedulesResponse\x12|\n\x0bhealth_ping\x12\x35.messaging.rpc.providers.grpc.proto.HealthPingRequest\x1a\x36.messaging.rpc.providers.grpc.proto.HealthPingResponseb\x06proto3'
  ,
  dependencies=[messages__pb2.DESCRIPTOR,])



_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_CLOCKNODESERVICE = _descriptor.ServiceDescriptor(
  name='ClockNodeService',
  full_name='messaging.rpc.providers.grpc.proto.clocknode.ClockNodeService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=90,
  serialized_end=647,
  methods=[
  _descriptor.MethodDescriptor(
    name='add_schedule',
    full_name='messaging.rpc.providers.grpc.proto.clocknode.ClockNodeService.add_schedule',
    index=0,
    containing_service=None,
    input_type=messages__pb2._ADDSCHEDULEREQUEST,
    output_type=messages__pb2._ADDSCHEDULERESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='remove_schedule',
    full_name='messaging.rpc.providers.grpc.proto.clocknode.ClockNodeService.remove_schedule',
    index=1,
    containing_service=None,
    input_type=messages__pb2._REMOVESCHEDULEREQUEST,
    output_type=messages__pb2._REMOVESCHEDULERESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='replace_schedules',
    full_name='messaging.rpc.providers.grpc.proto.clocknode.ClockNodeService.replace_schedules',
    index=2,
    containing_service=None,
    input_type=messages__pb2._REPLACESCHEDULESREQUEST,
    output_type=messages__pb2._REPLACESCHEDULESRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='health_ping',
    full_name='messaging.rpc.providers.grpc.proto.clocknode.ClockNodeService.health_ping',
    index=3,
    containing_service=None,
    input_type=messages__pb2._HEALTHPINGREQUEST,
    output_type=messages__pb2._HEALTHPINGRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_CLOCKNODESERVICE)

DESCRIPTOR.services_by_name['ClockNodeService'] = _CLOCKNODESERVICE

# @@protoc_insertion_point(module_scope)