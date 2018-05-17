# MinimaxTextGames
Text based games with numerous strategies including recursive and iterative minimax.
 
To play, run `game_interface.py`

## How It Works
### Overall Structure
The `game_interface.py` file relies on the generic Game and State classes in `game.py` and `state.py`, respectively. Therefore any game that can be made by subclassing these two classes can be played by `game_interface.py`. The games that can do this are generally two-player, sequential move, zero-sum, perfect-information games. 

If you do make your own game using these subclasses, make sure to add the Game class to the `playable_games` dictionary on line 11 of `game_interface.py`.

### Minimax
All the minimax strategies work by checking all possible moves from the current state, and picking a move that results in the highest possible 'score', or a move where if both players play perfectly, the current player will win. If this is not possible it picks a move where a tie results, or a loss as a last resort.

#### Recursive/Iterative
Both the recursive and iterative minimax strategies work by, either recursively or iteratively, looking through all possible moves and picking a move.

Since it does look through ALL possible moves, it can take a long time to run; for example, running minimax on a new Stonehenge Game of board size 3 can take over 4 hours to run.

#### Memoization
Memoization is similar to the recursive minimax strategy, however at each step of minimax, once a state's highest possible score has been found it gets added to a dictionary. Therefore, whenever we encounter a similiar state we already have it's score and don't have to do a recursive call on it.

This is one method of optimizing the recursive strategy to run faster/more efficiently.

#### Myopia
Myopia is also similar to the recursive minimax strategy, however it limits the depth of recursion to 4. Once depth 4 is reached, it determines a 'best_guess' using a state's rough_outcome() strategy of whether we think the state will result in a win, tie, or loss.

This method sacrifices accuracy for speed.
