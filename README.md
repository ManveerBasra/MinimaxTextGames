# MinimaxTextGames
Text based games with numerous strategies including recursive and iterative minimax.
 
To play, run `game_interface.py`

## How It Works
### Overall Structure
The `game_interface.py` file relies on the generic Game and State classes in `game.py` and `state.py`, respectively. Therefore any game that can be made by subclassing these two classes can be played by `game_interface.py`. The games that can do this are generally two-player, sequential move, zero-sum, perfect-information games. 

If you do make your own game using these subclasses, make sure to add the Game class to the `playable_games` dictionary on line 11 of `game_interface.py`.

### Minimax
Both the minimax strategies work by, either recursively or iteratively, looking through all possible moves and picking a move that results in the highest possible 'score', or a move where if both players play perfectly, the current player will win.

Since it does look through ALL possible moves, it can take a long time to run; for example, running minimax on a new Stonehenge Game of board size 3 can take over 4 hours to run. I am currently working on optimizing this algorithm.
