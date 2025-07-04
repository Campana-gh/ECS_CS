import core.lunar_lander
import key_strategy

strategy = key_strategy.KeyStrategy()
game = core.lunar_lander.Game(strategy, [strategy])
game.run()