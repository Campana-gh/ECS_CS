"""Play blackjack with a keyboard"""

import core.blackjack as blackjack
import key_strategy

strategy = key_strategy.KeyStrategy()
game = blackjack.Game(strategy, [strategy])
game.play()
