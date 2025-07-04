from assets.computer_basic import ComputerBasicStrategy
from button_strategy import ButtonStrategy
from core.nim_game import Game

b = ButtonStrategy()
game = Game(False, b, ComputerBasicStrategy(), [b])
game.__init__
game.run()
