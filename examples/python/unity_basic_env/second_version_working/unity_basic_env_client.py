"""The Python implementation of the gRPC for a basic Unity env."""

from __future__ import print_function

import logging
import random
import grpc
import unity_basic_env_pb2
import unity_basic_env_pb2_grpc


class DummyAgent:
  def __init__(self):
    self.is_connected = False
    self.num_timesteps = 0
    self.current_obs = None
    self.is_done = False
    self.episode_reward = 0
    self.episode_len = 0


def make_unity_basic_env_note(message, actionObs, reward, done):
  return unity_basic_env_pb2.UnityBasicEnvNote(
    message=message, actionObs=actionObs, reward=reward, done=done)


def generate_agent_action(obs):
  action = random.randint(-1, 1)
  if obs < 10:
    action *= action
  return action


def generate_step_message(action):
  messages = [make_unity_basic_env_note("action", action, 0., False)]
  for msg in messages:
    print("Sending start message {} aO/r/d {}/{}/{} ".format(msg.message, msg.actionObs, msg.reward, msg.done))
    yield msg


def unity_basic_env_step(stub, agent):
  agent.num_timesteps += 1
  action = generate_agent_action(agent.current_obs)
  print("sending step over {} with action {} based on obs {}".format(agent.num_timesteps, action, agent.current_obs))

  responses = stub.UnityBasicEnvChat(generate_step_message(action))
  for response in responses:
    if response.message == "step" or response.message == "reset":
      print("Receiving message {} o/r/d {}/{}/{} ".format(response.message, response.actionObs, response.reward,
                                                          response.done))
      agent.current_obs = response.actionObs
      agent.episode_reward += response.reward
      agent.episode_len += 1
      agent.done = response.done
      if agent.done:
        print("Episode is over rew {} | len {}".format(agent.episode_reward, agent.episode_len))
        agent.episode_len = 0
        agent.episode_reward = 0


def generate_start_message():
  messages = [make_unity_basic_env_note("start", 13, 0., False)]
  for msg in messages:
    print("Sending start message {} aO/r/d {}/{}/{} ".format(msg.message, msg.actionObs, msg.reward, msg.done))
    yield msg


def unity_basic_env_start(stub, agent):
  print("sending start message to server")
  responses = stub.UnityBasicEnvChat(generate_start_message())
  for response in responses:
    if response.message == "reset":
      print("Receiving message {} o/r/d {}/{}/{} ".format(response.message, response.actionObs, response.reward,
                                                          response.done))
      agent.is_connected = True
      agent.current_obs = response.actionObs
  print("start responses over")


def run():
  # NOTE(gRPC Python Team): .close() is possible on a channel and should be
  # used in circumstances in which the with statement does not fit the needs
  # of the code.
  with grpc.insecure_channel('localhost:50051') as channel:
    agent = DummyAgent()
    stub = unity_basic_env_pb2_grpc.UnityBasicEnvStub(channel)
    print("-------------- Starting UnityBasicEnv Client --------------")
    unity_basic_env_start(stub, agent)
    print("-------------- After start UnityBasicEnv Client --------------")
    for _ in range(10):
      print("in step loop ", agent.num_timesteps)
      unity_basic_env_step(stub, agent)
      print("in step look after stub")

    print("-------------- After step loop UnityBasicEnv Client --------------")
    # unit_basic_env_step(stub)
    # print("-------------- After step UnityBasicEnv Client --------------")


if __name__ == '__main__':
  logging.basicConfig()
  run()
