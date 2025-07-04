import soln.better_robot_strategy 
from core.nutgather import Game

strategy = soln.better_robot_strategy.BetterRobotStrategy()
game = Game(strategy)
game.run()