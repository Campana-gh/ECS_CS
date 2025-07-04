from assets.computer_advanced import ComputerAdvancedStrategy
from assets.computer_basic import ComputerBasicStrategy
from assets.computer_elite import ComputerEliteStrategy
from core.nim_game import Game
from human_strategy import HumanStrategy

human_strategy = HumanStrategy()
computer_difficulty = ComputerBasicStrategy()
game = Game(True, human_strategy, computer_difficulty, None, 1)
game.__init__
game.run()
