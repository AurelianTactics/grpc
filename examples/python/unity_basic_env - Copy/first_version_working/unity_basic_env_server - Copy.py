# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the gRPC basic env in Unity server."""

from concurrent import futures
import logging
import math
import time

import grpc
import unity_basic_env_pb2
import unity_basic_env_pb2_grpc


def make_unity_basic_env_note(message, actionObs, reward, done):
  return unity_basic_env_pb2.UnityBasicEnvNote(
    message=message, actionObs=actionObs, reward=reward, done=done)

class UnityBasicEnvServicer(unity_basic_env_pb2_grpc.UnityBasicEnvServicer):
    """Provides methods that implement functionality of unity basic env server."""

    def __init__(self):
      pass

    def UnityBasicEnvChat(self, request_iterator, context):
        prev_notes = []
        for new_note in request_iterator:
            for prev_note in prev_notes:
                yield prev_note
            prev_notes.append(new_note)
            print("adding new_note ", new_note.message)
            print("sendign response message ")
            yield make_unity_basic_env_note(message='server_response', actionObs=100, reward=100.1, done=False)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    unity_basic_env_pb2_grpc.add_UnityBasicEnvServicer_to_server(
        UnityBasicEnvServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
