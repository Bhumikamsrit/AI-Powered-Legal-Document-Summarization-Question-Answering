#!/usr/bin/env python3
import sys
from collections import defaultdict, deque

def solve_frog_maze():
    # Read input
    line = input().strip().split()
    n, m, k = int(line[0]), int(line[1]), int(line[2])
    
    # Read the maze
    maze = []
    for i in range(n):
        maze.append(input().strip())
    
    # Read tunnel connections
    tunnels = {}
    for _ in range(k):
        line = input().strip().split()
        r1, c1, r2, c2 = int(line[0]), int(line[1]), int(line[2]), int(line[3])
        tunnels[(r1, c1)] = (r2, c2)
        tunnels[(r2, c2)] = (r1, c1)
    
    # Find Alef's starting position
    start_pos = None
    for i in range(n):
        for j in range(m):
            if maze[i][j] == 'A':
                start_pos = (i, j)
                break
        if start_pos:
            break
    
    if not start_pos:
        return "0.000000"
    
    # Define directions (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Build graph of reachable states
    def get_neighbors(pos):
        r, c = pos
        neighbors = []
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < m and maze[nr][nc] != '#':
                neighbors.append((nr, nc))
        
        return neighbors
    
    # Apply tunnels - if a position has a tunnel, redirect to tunnel exit
    def apply_tunnel(pos):
        return tunnels.get(pos, pos)
    
    # Find all reachable positions
    visited = set()
    queue = deque([start_pos])
    reachable = set([start_pos])
    
    while queue:
        pos = queue.popleft()
        if pos in visited:
            continue
        visited.add(pos)
        
        neighbors = get_neighbors(pos)
        for neighbor in neighbors:
            final_pos = apply_tunnel(neighbor)
            if final_pos not in reachable:
                reachable.add(final_pos)
                queue.append(final_pos)
    
    # Separate positions by type
    free_positions = set()
    exit_positions = set()
    mine_positions = set()
    
    for pos in reachable:
        r, c = pos
        cell = maze[r][c]
        if cell in '.A':
            free_positions.add(pos)
        elif cell == '%':
            exit_positions.add(pos)
        elif cell == '*':
            mine_positions.add(pos)
    
    # If start position is an exit, probability is 1
    if start_pos in exit_positions:
        return "1.000000"
    
    # If start position is a mine, probability is 0
    if start_pos in mine_positions:
        return "0.000000"
    
    # Set up system of linear equations
    # For each free position, probability = average of probabilities of neighbors
    # For exit positions, probability = 1
    # For mine positions, probability = 0
    
    positions = list(free_positions)
    pos_to_idx = {pos: i for i, pos in enumerate(positions)}
    
    # Build coefficient matrix and constants vector
    n_vars = len(positions)
    if n_vars == 0:
        return "0.000000"
    
    # A * x = b where x is the vector of escape probabilities
    A = [[0.0] * n_vars for _ in range(n_vars)]
    b = [0.0] * n_vars
    
    for i, pos in enumerate(positions):
        neighbors = get_neighbors(pos)
        valid_neighbors = []
        
        for neighbor in neighbors:
            final_pos = apply_tunnel(neighbor)
            valid_neighbors.append(final_pos)
        
        if not valid_neighbors:
            # No valid moves - stuck (probability 0)
            A[i][i] = 1.0
            b[i] = 0.0
            continue
        
        # Set up equation: p[pos] = (1/k) * sum(p[neighbor])
        A[i][i] = len(valid_neighbors)  # Coefficient of p[pos]
        
        for neighbor_pos in valid_neighbors:
            r, c = neighbor_pos
            cell = maze[r][c]
            
            if cell == '%':  # Exit
                b[i] += 1.0
            elif cell == '*':  # Mine
                b[i] += 0.0
            elif neighbor_pos in pos_to_idx:  # Free position
                j = pos_to_idx[neighbor_pos]
                A[i][j] -= 1.0
    
    # Solve the system using Gaussian elimination
    def gaussian_elimination(matrix, constants):
        n = len(matrix)
        
        # Forward elimination
        for i in range(n):
            # Find pivot
            max_row = i
            for k in range(i + 1, n):
                if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                    max_row = k
            
            # Swap rows
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            constants[i], constants[max_row] = constants[max_row], constants[i]
            
            # Check for zero pivot
            if abs(matrix[i][i]) < 1e-10:
                continue
            
            # Eliminate column
            for k in range(i + 1, n):
                factor = matrix[k][i] / matrix[i][i]
                for j in range(i, n):
                    matrix[k][j] -= factor * matrix[i][j]
                constants[k] -= factor * constants[i]
        
        # Back substitution
        solution = [0.0] * n
        for i in range(n - 1, -1, -1):
            solution[i] = constants[i]
            for j in range(i + 1, n):
                solution[i] -= matrix[i][j] * solution[j]
            if abs(matrix[i][i]) > 1e-10:
                solution[i] /= matrix[i][i]
        
        return solution
    
    try:
        solution = gaussian_elimination(A, b)
        
        # Find the probability for the starting position
        if start_pos in pos_to_idx:
            prob = solution[pos_to_idx[start_pos]]
        else:
            prob = 0.0
        
        # Clamp probability to [0, 1]
        prob = max(0.0, min(1.0, prob))
        
        return f"{prob:.6f}"
    
    except:
        return "0.000000"

if __name__ == "__main__":
    result = solve_frog_maze()
    print(result)