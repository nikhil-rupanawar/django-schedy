#!/bin/bash


python3 -m grpc_tools.protoc -I=messaging/rpc/providers/grpc/proto/ --python_out=messaging/rpc/providers/grpc/interfaces/ --grpc_python_out=messaging/rpc/providers/grpc/interfaces/ messaging/rpc/providers/grpc/proto/messages.proto messaging/rpc/providers/grpc/proto/clocknode_service.proto messaging/rpc/providers/grpc/proto/registry_service.proto

#python3 -m grpc_tools.protoc -I=messaging/rpc/providers/grpc/proto/ --python_out=messaging/rpc/providers/grpc/interfaces/ --grpc_python_out=messaging/rpc/providers/grpc/interfaces/ messaging/rpc/providers/grpc/proto/clocknode_service.proto


