
from typing import Tuple, Set, List
from collections import deque
from board import HexBoard


class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id

    def play(self, board: HexBoard) -> tuple:
        raise NotImplementedError()


class PlayerMinimax(Player):
    def __init__(self, player_id: int):
        super().__init__(player_id)
        self.opponent_id = 1 if player_id == 2 else 2
        self.MAX_REWARD = float('inf')
        self.MIN_REWARD = -float('inf')
        self.directions = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]

    def play(self, board: HexBoard) -> tuple:
        return self.get_best_move(board)

    def get_best_move(self, board: HexBoard, depth: int = 3) -> Tuple[int, int]:
        best_move = None
        alpha = self.MIN_REWARD
        beta = self.MAX_REWARD

        for move in board.get_possible_moves():
            new_board = board.clone()
            new_board.place_piece(move[0], move[1], self.player_id)

            score = self.minimax(new_board, depth-1, alpha, beta, False)

            if score > alpha:
                alpha = score
                best_move = move

        return best_move if best_move else board.get_possible_moves()[0]

    def minimax(self, board: HexBoard, depth: int, alpha: float, beta: float, maximizing_player: bool) -> float:
        if board.check_connection(self.player_id):
            return 0
        if board.check_connection(self.opponent_id):
            return -self.MAX_REWARD
        if depth == 0:
            return self.evaluate_position(board)

        possible_moves = board.get_possible_moves()
        if not possible_moves:
            return 0

        if maximizing_player:
            max_eval = self.MIN_REWARD
            for move in possible_moves:
                new_board = board.clone()
                new_board.place_piece(move[0], move[1], self.player_id)
                current_eval = self.minimax(new_board, depth-1, alpha, beta, False)

                max_eval = max(max_eval, current_eval)
                alpha = max(alpha, current_eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = self.MAX_REWARD
            for move in possible_moves:
                new_board = board.clone()
                new_board.place_piece(move[0], move[1], self.opponent_id)
                current_eval = self.minimax(new_board, depth-1, alpha, beta, True)

                min_eval = min(min_eval, current_eval)
                beta = min(beta, current_eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate_position(self, board: HexBoard) -> float:
        if board.check_connection(self.player_id):
            return 0
        if board.check_connection(self.opponent_id):
            return -self.MAX_REWARD

        d_player = self.estimate_cost(board, self.player_id)
        d_opponent = self.estimate_cost(board, self.opponent_id)
        center_advantage = self.evaluate_center_control(board)

        return d_player - 0.8 * d_opponent + 0.01 * center_advantage

    def estimate_cost(self, board: HexBoard, player_id: int) -> float:
        components = self.get_connected_components(board, player_id)
        size = board.size
        min_distance = size

        if player_id == 1:
            start_side = [(i, 0) for i in range(size)]
            end_side = [(i, size-1) for i in range(size)]
        else:
            start_side = [(0, j) for j in range(size)]
            end_side = [(size-1, j) for j in range(size)]

        if not components:
            return self.shortest_path(board, set(start_side), end_side, player_id)

        for component in components:
            touches_start = any((pos[1] == 0 if player_id == 1 else pos[0] == 0) for pos in component)
            if touches_start:
                distance = self.shortest_path(board, component, end_side, player_id)
                min_distance = min(min_distance, distance)

        return min_distance

    def shortest_path(self, board: HexBoard, start_nodes: Set[Tuple[int, int]], end_side: List[Tuple[int, int]], player_id: int) -> float:
        size = board.size
        queue = deque([(node, 0) for node in start_nodes])
        visited = set(start_nodes)
        end_set = set(end_side)

        while queue:
            (row, col), dist = queue.popleft()

            if (row, col) in end_set:
                return dist

            for dx, dy in self.directions:
                new_row, new_col = row + dx, col + dy
                if 0 <= new_row < size and 0 <= new_col < size:
                    if (new_row, new_col) not in visited and board.board[new_row][new_col] != self.opponent_id:
                        visited.add((new_row, new_col))
                        queue.append(((new_row, new_col), dist + 1))

        return size

    def evaluate_center_control(self, board: HexBoard) -> float:
        size = board.size
        center = size // 2
        radius = size // 3
        c_player, c_opponent = 0, 0
        total_cells = 0
        for i in range(max(0, center-radius), min(size, center+radius+1)):
            for j in range(max(0, center-radius), min(size, center+radius+1)):
                if board.board[i][j] == self.player_id:
                    c_player += 1
                elif board.board[i][j] == self.opponent_id:
                    c_opponent += 1
                total_cells += 1
        return (c_player - c_opponent) / total_cells if total_cells > 0 else 0

    def get_connected_components(self, board: HexBoard, player_id: int) -> List[Set[Tuple[int, int]]]:
        visited = set()
        components = []

        for i in range(board.size):
            for j in range(board.size):
                if board.board[i][j] == player_id and (i, j) not in visited:
                    stack = [(i, j)]
                    component = set()
                    while stack:
                        row, col = stack.pop()
                        if (row, col) in visited:
                            continue
                        visited.add((row, col))
                        component.add((row, col))
                
                        for dx, dy in self.directions:
                            new_row, new_col = row + dx, col + dy
                            if (0 <= new_row < board.size and 
                                0 <= new_col < board.size and 
                                board.board[new_row][new_col] == player_id):
                                stack.append((new_row, new_col))
                    components.append(component)
        return components 

