from player import Player
from board import HexBoard

class HumanPlayer(Player):
    def __init__(self, player_id: int):
        super().__init__(player_id)

    def play(self, board: HexBoard) -> bool:
        while True:
            try:
                row, col = map(
                    int,
                    input(
                        f"Player {self.player_id}, enter your move (row col): "
                    ).split(),
                )
                if 0 <= row < board.size and 0 <= col < board.size and board.board[row][col] == 0:
                    return row, col
                else:
                    print("Invalid move! Try again.")
            except ValueError:
                print("Invalid input! Please enter numbers for row and column.")
            except KeyboardInterrupt:
                print("\nGame interrupted. Exiting...")
                exit(0)