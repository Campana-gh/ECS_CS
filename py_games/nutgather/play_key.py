import key_strategy
from core.nutgather import Game

strategy = key_strategy.KeyStrategy()
game = Game(strategy)
game.run()