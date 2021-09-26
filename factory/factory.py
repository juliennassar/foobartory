import random
from datetime import datetime

from .robot import Robot
from .product import Foo, Bar, FooBar
from .config import *


class Factory:
    """
    Foobar Factory
    """

    def __init__(self):
        self.foo: list = []
        self.bar: list = []
        self.foobar: list = []
        self.cash: int = 0
        self.robots: list = []
        self.start_time: datetime = datetime.now()

    @property
    def foo_stock(self):
        """
        get the current foo stock count
        :return: int - foo stock count
        """
        return len(self.foo)

    @property
    def bar_stock(self):
        """
        get the current bar stock count
        :return: int - bar stock count
        """
        return len(self.bar)

    @property
    def foobar_stock(self):
        """
        get the current foobar stock count
        :return: int - foobar stock count
        """
        return len(self.foobar)

    @property
    def foo_miner_count(self):
        """
        get the current number of robots mining foos
        :return: int - number of robots mining foos
        """
        return len(list(filter(lambda x: x.type == FOO_MINER, self.robots)))

    @property
    def bar_miner_count(self):
        """
        get the current number of robots mining bars
        :return: int - number of robots mining bars
        """
        return len(list(filter(lambda x: x.type == BAR_MINER, self.robots)))

    @property
    def assembler_count(self):
        """
        get the current number of robots assembling FooBars
        :return: int - number of robots assembling FooBars
        """
        return len(list(filter(lambda x: x.type == ASSEMBLER, self.robots)))

    @property
    def seller_count(self):
        """
        get the current number of robots selling foobars
        :return: int - number of robots selling foobars
        """
        return len(list(filter(lambda x: x.type == SELLER, self.robots)))

    @property
    def buyer_count(self):
        """
        get the current number of robots buying robots
        :return: int - number of robots buying robots
        """
        return len(list(filter(lambda x: x.type == BUYER, self.robots)))

    def display(self):
        """
        Display on terminal the current factory status
        """
        rep = f'foo stock: {self.foo_stock}\tbar stock: {self.bar_stock}\tfoobar stock: {self.foobar_stock}\n' \
              f'robots : {len(self.robots)}\tcash: {self.cash}\n' \
              f'foo miners: {self.foo_miner_count}\tbar miners: {self.bar_miner_count}\t' \
              f'assemblers: {self.assembler_count}\tsellers: {self.seller_count}\t' \
              f'buyers: {self.buyer_count}\nelapsed time: {datetime.now() - self.start_time}'
        print(rep)

    def mine_foo(self):
        """
        Foo mining job, grants 1 level point per foo mines
        :returns : int - 1 level point per foo mined
        """
        self.foo.append(Foo())
        return 1

    def mine_bar(self):
        """
        Bar mining job, grants 1 level point per bar mined
        :returns : int - 1 level point per foo mined
        """
        self.bar.append(Bar())
        return 1

    def assemble(self):
        """
        Assembly job, grants 1 level point per FooBar successfully assembled
        :returns : int - 1 level point per foobar successfully assembled
        """
        if self.foo_stock < 1 or self.bar_stock < 1:
            return 0

        # implements the random failure event when assembling a FooBar
        if random.random() < 0.4:
            self.foo.pop()
            return 0

        foo = self.foo.pop()
        bar = self.bar.pop()
        self.foobar.append(FooBar(foo, bar))
        return 1

    def sell(self):
        """
        Seller job, grants 1 level point per FooBar sold
        :returns : int - 1 level point per foobar sold
        """
        if self.foobar_stock < 1:
            return 0

        qtt = min(5, self.foobar_stock)
        for _ in range(qtt):
            self.foobar.pop()
        self.cash += qtt
        return qtt

    def buy(self):
        """
        Seller job, grants 1 level point per Robot bought
        :returns : int - 1 level point per robot bought
        """
        if self.foo_stock < 6 or self.cash < 3:
            return 0

        for _ in range(6):
            self.foo.pop()
        self.cash -= 3

        Robot(self)
        return 1

    def register(self, robot):
        """
        adds a robot to the factory
        :param robot: Robot to add to the factory
        """
        self.robots.append(robot)

    def promote(self, robot):
        """
        This method enables robots to go from Foo miner, to Bar miner, assembler, seller and buyer depending on his
        level and available positions in the chain.
        :param robot: Robot to promote
        :return: bool - if the robot was promoted or not
        """
        if robot.type != FOO_MINER and robot.level < MAX_LEVEL[FOO_MINER]:
            self.promote_foo_miner(robot)
            return True
        if robot.type != BAR_MINER and (MAX_LEVEL[FOO_MINER] <= robot.level < MAX_LEVEL[BAR_MINER]) and \
                self.bar_miner_count * 2 < self.foo_miner_count:
            self.promote_bar_miner(robot)
            return True
        if robot.type != ASSEMBLER and (MAX_LEVEL[BAR_MINER] <= robot.level < MAX_LEVEL[ASSEMBLER]) and \
                self.assembler_count < min(MAX_JOBS[ASSEMBLER], self.bar_miner_count):
            self.promote_assembler(robot)
            return True
        if robot.type != SELLER and (MAX_LEVEL[ASSEMBLER] <= robot.level < MAX_LEVEL[SELLER]) and \
                self.seller_count < min(MAX_JOBS[SELLER], self.assembler_count):
            self.promote_seller(robot)
            return True
        if robot.type != BUYER and robot.level >= MAX_LEVEL[SELLER] and self.buyer_count < MAX_JOBS[BUYER]:
            self.promote_buyer(robot)
            return True
        return False

    def promote_foo_miner(self, robot):
        """
        promotion to foo miner
        :param robot: Robot to promote
        """
        robot.type = FOO_MINER
        robot.get_task_duration = lambda: 1
        robot.perform_task = self.mine_foo

    def promote_bar_miner(self, robot):
        """
        promotion to bar miner
        :param robot: Robot to promote
        """
        robot.type = BAR_MINER
        robot.get_task_duration = lambda: random.random() * 1.5 + 0.5
        robot.perform_task = self.mine_bar

    def promote_assembler(self, robot):
        """
        promotion to assembler
        :param robot: Robot to promote
        """
        robot.type = ASSEMBLER
        robot.get_task_duration = lambda: 2
        robot.perform_task = self.assemble

    def promote_seller(self, robot):
        """
        promotion to seller
        :param robot: Robot to promote
        """
        robot.type = SELLER
        robot.get_task_duration = lambda: 10
        robot.perform_task = self.sell

    def promote_buyer(self, robot):
        """
        promotion to buyer
        :param robot: Robot to promote
        """
        robot.type = BUYER
        robot.get_task_duration = lambda: 0
        robot.perform_task = self.buy
