from assets.computer_advanced import ComputerAdvancedStrategy
from button_strategy import ButtonStrategy
from core.nim_game import Game

b = ButtonStrategy()
game = Game(False, b, ComputerAdvancedStrategy(), [b])
game.__init__
game.run()
