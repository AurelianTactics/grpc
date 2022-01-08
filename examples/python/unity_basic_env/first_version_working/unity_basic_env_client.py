"""The Python implementation of the gRPC for a basic Unity env."""

from __future__ import print_function

import logging
import random
import grpc
import unity_basic_env_pb2
import unity_basic_env_pb2_grpc


def make_unity_basic_env_note(message, actionObs, reward, done):
    return unity_basic_env_pb2.UnityBasicEnvNote(
        message=message, actionObs=actionObs, reward=reward, done=done)


def generate_messages():
    messages = [
        make_unity_basic_env_note("step_result", 0, 0.1, True),
        make_unity_basic_env_note("step_result", 13, -0.1, False),
        make_unity_basic_env_note("step_result", 20, 1., True),
    ]
    for msg in messages:
        print("Sending {} a/r/d {}/{}/{} ".format(msg.message, msg.actionObs, msg.reward, msg.done))
        yield msg


def unit_basic_env_chat(stub):
    responses = stub.UnityBasicEnvChat(generate_messages())
    for response in responses:
        print("Receiving {} o/r/d {}/{}/{} ".format(response.message, response.actionObs, response.reward,
                                                    response.done))


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = unity_basic_env_pb2_grpc.UnityBasicEnvStub(channel)
        print("-------------- UnityBasicEnvChat --------------")
        unit_basic_env_chat(stub)


if __name__ == '__main__':
    logging.basicConfig()
    run()
