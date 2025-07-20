#!/usr/bin/env python3

from fractions import Fraction

if __name__ == '__main__':
    first_multiple_input = input().rstrip().split()
    
    n = int(first_multiple_input[0])
    m = int(first_multiple_input[1]) 
    k = int(first_multiple_input[2])
    
    maze = []
    start_pos = None
    
    for n_itr in range(n):
        row = input()
        maze.append(row)
        # Write your code here
        for j, cell in enumerate(row):
            if cell == 'A':
                start_pos = (n_itr, j)
    
    tunnels = {}
    for k_itr in range(k):
        second_multiple_input = input().rstrip().split()
        
        i1 = int(second_multiple_input[0])
        j1 = int(second_multiple_input[1])
        i2 = int(second_multiple_input[2])
        j2 = int(second_multiple_input[3])
        
        # Write your code here
        # Convert to 0-based indexing
        i1 -= 1
        j1 -= 1
        i2 -= 1
        j2 -= 1
        
        tunnels[(i1, j1)] = (i2, j2)
        tunnels[(i2, j2)] = (i1, j1)
    
    # Write your code here
    
    # Map positions to state indices
    pos_to_state = {}
    state_to_pos = {}
    state_count = 0
    
    for i in range(n):
        for j in range(m):
            if maze[i][j] != '#':
                pos_to_state[(i, j)] = state_count
                state_to_pos[state_count] = (i, j)
                state_count += 1
    
    # Build transition matrix for Markov chain
    total_states = state_count + 2  # +2 for escape and death states
    escape_state = state_count
    death_state = state_count + 1
    
    transitions = [[Fraction(0) for _ in range(total_states)] for _ in range(total_states)]
    
    # Absorbing states
    transitions[escape_state][escape_state] = Fraction(1)
    transitions[death_state][death_state] = Fraction(1)
    
    # Build transitions
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    for state in range(state_count):
        i, j = state_to_pos[state]
        cell = maze[i][j]
        
        if cell == '%':  # Exit
            transitions[state][escape_state] = Fraction(1)
            continue
        elif cell == '*':  # Mine
            transitions[state][death_state] = Fraction(1)
            continue
        
        # Find valid moves
        valid_moves = []
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < m and maze[ni][nj] != '#':
                valid_moves.append((ni, nj))
        
        if not valid_moves:
            transitions[state][death_state] = Fraction(1)
            continue
        
        prob = Fraction(1, len(valid_moves))
        
        for ni, nj in valid_moves:
            target_cell = maze[ni][nj]
            
            # Check for tunnel
            if (ni, nj) in tunnels:
                tunnel_exit = tunnels[(ni, nj)]
                target_state = pos_to_state[tunnel_exit]
                transitions[state][target_state] += prob
            else:
                if target_cell == '%':
                    transitions[state][escape_state] += prob
                elif target_cell == '*':
                    transitions[state][death_state] += prob
                else:
                    target_state = pos_to_state[(ni, nj)]
                    transitions[state][target_state] += prob
    
    # Solve linear system (I - Q)x = r
    start_state = pos_to_state[start_pos]
    size = state_count
    
    # Create augmented matrix
    matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            if i == j:
                row.append(Fraction(1) - transitions[i][j])
            else:
                row.append(-transitions[i][j])
        row.append(transitions[i][escape_state])  # RHS
        matrix.append(row)
    
    # Gaussian elimination
    for i in range(size):
        # Find pivot
        max_row = i
        for k in range(i + 1, size):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate column
        for k in range(i + 1, size):
            if matrix[i][i] != 0:
                factor = matrix[k][i] / matrix[i][i]
                for j in range(i, size + 1):
                    matrix[k][j] -= factor * matrix[i][j]
    
    # Back substitution
    solution = [Fraction(0)] * size
    for i in range(size - 1, -1, -1):
        solution[i] = matrix[i][size]
        for j in range(i + 1, size):
            solution[i] -= matrix[i][j] * solution[j]
        if matrix[i][i] != 0:
            solution[i] /= matrix[i][i]
    
    result = float(solution[start_state])
    print(f"{result:.10f}")