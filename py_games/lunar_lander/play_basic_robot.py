import core.lunar_lander
import basic_robot_strategy

strategy = basic_robot_strategy.BasicRobotStrategy()
game = core.lunar_lander.Game(strategy, [], 1000)
game.run()