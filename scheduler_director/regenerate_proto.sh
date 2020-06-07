#!/bin/bash

python3 -m grpc_tools.protoc -Imessaging/rpc/providers/grpc/proto --python_out=messaging/rpc/providers/grpc/interfaces/ --grpc_python_out=messaging/rpc/providers/grpc/interfaces/ messaging/rpc/providers/grpc/proto/clocknode.proto

