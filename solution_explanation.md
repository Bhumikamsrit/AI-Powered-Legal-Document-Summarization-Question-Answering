# Frog in Maze Solution

## Problem Overview
This problem asks us to calculate the probability that Alef the Frog escapes from a maze. The frog moves randomly with equal probability to any adjacent free cell.

## Algorithm Approach

The solution uses **Markov Chain** theory to model the problem as a system of linear equations.

### Key Steps:

1. **Parse Input**: Read maze dimensions, maze layout, and tunnel connections
2. **Find Reachable States**: Use BFS to find all positions reachable from the starting position
3. **Classify Positions**: 
   - Free cells (`.` or `A`): Can move to adjacent cells
   - Exit cells (`%`): Escape probability = 1
   - Mine cells (`*`): Escape probability = 0
   - Obstacles (`#`): Cannot be entered

4. **Set up Linear System**: For each free position, the escape probability equals the average of escape probabilities of all adjacent positions:
   ```
   P(position) = (1/k) × Σ P(adjacent_positions)
   ```

5. **Handle Tunnels**: When a frog lands on a tunnel entrance, it's immediately transported to the tunnel exit

6. **Solve System**: Use Gaussian elimination to solve the system of linear equations

### Mathematical Model

For a maze with n free positions, we have n equations of the form:
- `P[i] = (1/deg[i]) × Σ P[neighbors[i]]` for free positions
- `P[exit] = 1` for exit positions  
- `P[mine] = 0` for mine positions

This creates a system `A × P = b` where P is the vector of escape probabilities.

### Time Complexity
- O(n³) for Gaussian elimination where n is the number of free cells
- O(nm) for maze parsing and BFS

The solution handles edge cases like:
- Starting on an exit (probability = 1)
- Starting on a mine (probability = 0)  
- Unreachable exits
- Cycles in the maze