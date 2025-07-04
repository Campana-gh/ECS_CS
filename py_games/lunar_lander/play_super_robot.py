import core.lunar_lander
import soln.super_robot_strategy

strategy = soln.super_robot_strategy.SuperRobotStrategy()
game = core.lunar_lander.Game(strategy, [])
game.run()