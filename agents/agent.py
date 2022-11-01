from api import agent_api
from api.command import Command
from craftbots.entities.actor import Actor
from craftbots.log_manager import Logger

class Agent:

    def __init__(self):

        # simulation status flags
        self.simulation_complete = False
        self.simulation_paused = False

        # simulation interface
        self.api : agent_api.AgentAPI = None  # type: ignore
        self.world_info : dict = None  # type: ignore

        # agent status flag
        self.thinking = False            

    def get_next_commands(self):
        pass