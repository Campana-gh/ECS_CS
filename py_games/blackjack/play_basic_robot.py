"""Play blackjack with a robot (a simple one)"""

import basic_robot_strategy
import core.blackjack as blackjack

strategy = basic_robot_strategy.BasicRobotStrategy()
game = blackjack.Game(strategy)
game.play()
