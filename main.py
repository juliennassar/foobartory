import os
import time
from factory.robot import Robot
from factory.factory import Factory


def play():
    """
    Play method to run the factory simulation
    """
    # Initialize the factory with empty stocks and 2 robots
    my_factory = Factory()
    Robot(my_factory)
    Robot(my_factory)

    # Loop while goal is not achieve : 30 robots in the factory
    while len(my_factory.robots) < 30:
        # I am using non blocking synchronous task management
        for cur_robot in my_factory.robots:
            cur_robot.run()

        # I hope this line will work out for you to get a clear view of the factory status on a clean terminal!
        os.system('cls' if os.name == 'nt' else 'clear')
        my_factory.display()
        # I run 10 loops/sec, this can be increased but will not change the simulation speed as task time rely on
        # actual timestamp
        time.sleep(0.1)


if __name__ == '__main__':
    play()
