from assets.computer_elite import ComputerEliteStrategy
from button_strategy import ButtonStrategy
from core.nim_game import Game

b = ButtonStrategy()
game = Game(False, b, ComputerEliteStrategy(), [b])
game.__init__
game.run()
