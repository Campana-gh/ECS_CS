A collection of pygame programs as part of the ECS CS program. The games all require python3 and pygame to be installed.

The students are expected to play the game with the keyboard initially to get a feel for the game. After that, they should modify the student_strategy to see if they can win the game.

In general, the structure of the directories should be.

assets - any video, images, sound used by the game
core - the main game and scaffolding code. Students aren't expected to edit this.
soln - the teacher strategy is implmented here. "Hidden" so that the student's can't easily look at it.
xxx_strategy - an implementation of the strategy for one of the players.
   key_strategy - play the game with the keyboard
   robot_strategy - the code to play the game
play_xxx - a simple python wrapper to play that version of the game. For example, "python3 play_keyboard.py" will play the keyboard version.

