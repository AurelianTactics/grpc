"""The Python implementation of the gRPC basic env in Unity server."""

from concurrent import futures
import logging
import math
import time
import random
import grpc
import unity_basic_env_pb2
import unity_basic_env_pb2_grpc


# shows how to set up env with some sort of config
def init_env(message, config_value):
  if message == 'start':
    print("starting env with config_value ", config_value)
    # to do: set up env with config values


def reset_env():
  return make_unity_basic_env_note("reset", 10, -0.1, False)


def make_unity_basic_env_note(message, actionObs, reward, done):
  return unity_basic_env_pb2.UnityBasicEnvNote(
    message=message, actionObs=actionObs, reward=reward, done=done)


class UnityBasicEnvServicer(unity_basic_env_pb2_grpc.UnityBasicEnvServicer):
  """Provides methods that implement functionality of unity basic env server."""

  def __init__(self):
    self.is_done = False

  def UnityBasicEnvChat(self, request_iterator, context):
    # print("got message in unitybasicenvstep 0")
    for step in request_iterator:
      # print("got message in unitybasicenvstep 1")
      if step.message == "action":
        yield self.handle_action(step.actionObs)
        if self.is_done:
          yield reset_env()
      elif step.message == "start":
        # print("got message in unitybasicenvstep 2")
        init_env(step.message, step.actionObs)
        yield reset_env()

  def handle_action(self, action):
    if action == 1:
      obs = random.randint(10, 20)
    else:
      obs = random.randint(0, 20)

    if obs >= 15:
      done = True
      reward = 1.0
    else:
      done = False
      reward = -0.1
    self.is_done = done
    print("received action, sending back step info")
    return make_unity_basic_env_note("step", obs, reward, done)


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  unity_basic_env_pb2_grpc.add_UnityBasicEnvServicer_to_server(
    UnityBasicEnvServicer(), server)
  server.add_insecure_port('[::]:30051')
  server.start()
  print("-------------- Server Start UnityBasicEnvServer --------------")
  server.wait_for_termination()


if __name__ == '__main__':
  logging.basicConfig()
  serve()
