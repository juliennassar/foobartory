import uuid
from datetime import datetime, timedelta

from .config import *


class Robot:
    """
    Robot worker class
    """
    def __init__(self, my_factory):
        self.factory = my_factory
        self.factory.register(self)
        self.robot_id = uuid.uuid4()

        self.get_task_duration: callable = None
        self.busy_until: datetime = datetime.now()
        self.perform_task: callable = None
        self.get_reward_when_done: bool = False
        self.level: int = 0
        self.type: str = 'NONE'

    def run(self):
        """
        Method to run the robot in the factory so it performs its assigned task
        """
        if self.busy_until > datetime.now():
            return

        if self.factory.promote(self):
            self.busy_until = datetime.now() + timedelta(seconds=5)
            return

        # This conditions enforces to perform the work only when the robot has spent enough time on his task
        if self.get_reward_when_done:
            # The task method returns the number of level point the robot gets for successfully performing a task
            points = self.perform_task()
            # we don't allow the robot to go past the max job title level to avoid job hopping
            self.level = min(MAX_LEVEL[self.type], self.level + points)
            self.get_reward_when_done = False

        self.busy_until = datetime.now() + timedelta(seconds=self.get_task_duration())
        self.get_reward_when_done = True
