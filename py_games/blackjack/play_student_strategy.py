import core.blackjack as blackjack
import student_strategy

strategy = student_strategy.StudentStrategy()
game = blackjack.Game(strategy, [strategy])
game.play()