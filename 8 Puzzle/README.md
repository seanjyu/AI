# 8 Puzzle Solver

The code uses 3 different search algorithims to solve the 8 puzzle, namely bfs, dfs and A-star search. The manhattan heuristic was used as the heuristic for the A-star search. 

The code intakes a string that represents the board and finds the shortest path based on the search algorithm used.
Below shows the board and equivalent string for a goal state and an example problem state.

![](images/image1.png)

The output of the code is a text file which contains the path, nodes expanded, search depth, max search depth, running time and max ram usage. To run this code search method and the board is inputed. An example execution code could be 'python3 puzzle.py bfs 2,8,1,3,5,4,6,0,7'

Below shows an example output file.
![](images/image2.png)
