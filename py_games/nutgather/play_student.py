import student_strategy
from core.nutgather import Game

strategy = student_strategy.StudentStrategy()
game = Game(strategy)
game.run()