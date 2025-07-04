"""Play blackjack with a robot (a good one)"""

import soln.better_robot_strategy
import core.blackjack as blackjack

strategy = soln.better_robot_strategy.BetterRobotStrategy()
game = blackjack.Game(strategy)
game.play()
