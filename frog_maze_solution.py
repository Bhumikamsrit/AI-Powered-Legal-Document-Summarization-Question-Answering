#!/usr/bin/env python3

import sys
from fractions import Fraction

def solve_frog_maze():
    # Read input exactly as shown in the template
    first_multiple_input = input().rstrip().split()
    n = int(first_multiple_input[0])
    m = int(first_multiple_input[1])
    k = int(first_multiple_input[2])
    
    # Read the maze
    maze = []
    start_pos = None
    
    for n_itr in range(n):
        row = input().rstrip()
        maze.append(row)
        # Find the starting position 'A'
        for j, cell in enumerate(row):
            if cell == 'A':
                start_pos = (n_itr, j)
    
    # Read tunnel connections
    tunnels = {}
    for k_itr in range(k):
        second_multiple_input = input().rstrip().split()
        i1 = int(second_multiple_input[0]) - 1  # Convert to 0-based indexing
        j1 = int(second_multiple_input[1]) - 1
        i2 = int(second_multiple_input[2]) - 1
        j2 = int(second_multiple_input[3]) - 1
        
        tunnels[(i1, j1)] = (i2, j2)
        tunnels[(i2, j2)] = (i1, j1)
    
    # Map positions to state indices
    pos_to_state = {}
    state_to_pos = {}
    state_count = 0
    
    for i in range(n):
        for j in range(m):
            if maze[i][j] != '#':  # Not an obstacle
                pos_to_state[(i, j)] = state_count
                state_to_pos[state_count] = (i, j)
                state_count += 1
    
    # Build transition matrix
    # States: 0 to state_count-1 (transient), state_count (escape), state_count+1 (death)
    total_states = state_count + 2
    escape_state = state_count
    death_state = state_count + 1
    
    # Initialize transition matrix
    transitions = [[Fraction(0) for _ in range(total_states)] for _ in range(total_states)]
    
    # Set absorbing states
    transitions[escape_state][escape_state] = Fraction(1)
    transitions[death_state][death_state] = Fraction(1)
    
    # Build transitions for each non-obstacle cell
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up
    
    for state in range(state_count):
        i, j = state_to_pos[state]
        cell = maze[i][j]
        
        # If this is an exit or mine, it's absorbing
        if cell == '%':  # Exit
            transitions[state][escape_state] = Fraction(1)
            continue
        elif cell == '*':  # Mine
            transitions[state][death_state] = Fraction(1)
            continue
        
        # Count valid moves
        valid_moves = []
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < m and maze[ni][nj] != '#':
                valid_moves.append((ni, nj))
        
        if not valid_moves:  # Stuck (shouldn't happen in valid input)
            transitions[state][death_state] = Fraction(1)
            continue
        
        # Equal probability for each valid move
        prob = Fraction(1, len(valid_moves))
        
        for ni, nj in valid_moves:
            target_cell = maze[ni][nj]
            
            # Check if this move goes through a tunnel
            if (ni, nj) in tunnels:
                # Tunnel entrance - go to the other end
                tunnel_exit = tunnels[(ni, nj)]
                target_state = pos_to_state[tunnel_exit]
            else:
                # Normal move
                if target_cell == '%':  # Exit
                    transitions[state][escape_state] += prob
                    continue
                elif target_cell == '*':  # Mine
                    transitions[state][death_state] += prob
                    continue
                else:
                    target_state = pos_to_state[(ni, nj)]
            
            transitions[state][target_state] += prob
    
    # Solve the system using Gaussian elimination
    # We want to find the probability of reaching escape_state from start_pos
    start_state = pos_to_state[start_pos]
    
    # Create system: (I - Q) * x = r
    # where Q is the transient-to-transient part, r is transient-to-escape part
    size = state_count
    matrix = []
    rhs = []
    
    for i in range(size):
        row = []
        for j in range(size):
            if i == j:
                row.append(Fraction(1) - transitions[i][j])
            else:
                row.append(-transitions[i][j])
        matrix.append(row)
        rhs.append(transitions[i][escape_state])
    
    # Gaussian elimination with partial pivoting
    for i in range(size):
        # Find pivot
        max_row = i
        for k in range(i + 1, size):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        rhs[i], rhs[max_row] = rhs[max_row], rhs[i]
        
        # Make all rows below this one 0 in current column
        for k in range(i + 1, size):
            if matrix[i][i] != 0:
                factor = matrix[k][i] / matrix[i][i]
                for j in range(i, size):
                    matrix[k][j] -= factor * matrix[i][j]
                rhs[k] -= factor * rhs[i]
    
    # Back substitution
    solution = [Fraction(0)] * size
    for i in range(size - 1, -1, -1):
        solution[i] = rhs[i]
        for j in range(i + 1, size):
            solution[i] -= matrix[i][j] * solution[j]
        if matrix[i][i] != 0:
            solution[i] /= matrix[i][i]
    
    # Return probability for start state
    result = float(solution[start_state])
    return result

if __name__ == '__main__':
    result = solve_frog_maze()
    print(f"{result:.10f}")