from __future__ import annotations
import copy

class HexBoard:
    def __init__(self, size: int):
        self.size = size  
        self.board = [[0 for _ in range(size)] for _ in range(size)]  
    def clone(self) -> HexBoard:
        return copy.deepcopy(self) 
    
    def place_piece(self, row: int, col: int, player_id: int) -> bool:
        if self.board[row][col] == 0 :
            self.board[row][col] = player_id
            return True
        else:
            return False
    
    def get_possible_moves(self) -> list:
        possible_moves = []
        
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell == 0:  
                    possible_moves.append((i, j))
        
        return possible_moves   

    def check_connection(self, player_id: int) -> bool:
        visited = set()
        queue = []
        size = self.size

        if player_id == 2:
            start_nodes = [(0, col) for col in range(size) if self.board[0][col] == player_id]
            target_row = size - 1
        else:
            start_nodes = [(row, 0) for row in range(size) if self.board[row][0] == player_id]
            target_col = size - 1

        queue.extend(start_nodes)
        visited.update(start_nodes)

        while queue:
            row, col = queue.pop(0)

            if (player_id == 1 and col == target_col) or (player_id == 2 and row == target_row):
                return True

            for dr, dc in [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]:
                new_row, new_col = row + dr, col + dc
                if (0 <= new_row < size and 0 <= new_col < size and
                        self.board[new_row][new_col] == player_id and
                        (new_row, new_col) not in visited):
                    visited.add((new_row, new_col))
                    queue.append((new_row, new_col))

        return False
    
    def print_board(self):
        for i, row in enumerate(self.board):
            print("  " * i, end="")  
            
            for j, cell in enumerate(row):
                if cell == 1:
                    print("🔴", end="  ")
                elif cell == 2:
                    print("🔵", end="  ")
                else:
                    print("⚪", end="  ")
            print()  



