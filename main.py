from board import HexBoard
from player import PlayerMinimax
from human_player import HumanPlayer

def get_board_size() -> int:
    while True:
        try:
            size = int(input("Ingresa el tamaño del tablero (mínimo 3): "))
            if size >= 3:
                return size
            else:
                print("El tamaño debe ser al menos 3")
        except ValueError:
            print("Por favor ingresa un número válido") 

def main():
    size = get_board_size()
    board = HexBoard(size=size)
    human_player = HumanPlayer(player_id=1)
    ai_player = PlayerMinimax(player_id=2)
    
    print("\n=== Bienvenido al juego Hex ===")
    print("Jugador 1 (🔴) - Humano: Conecta de izquierda a derecha")
    print("Jugador 2 (🔵) - AI: Conecta de arriba a abajo")
    print("================================\n")
    
    current_turn = 0
    
    while True:
        board.print_board()
        
        if current_turn == 0:
            print("\nTurno del Jugador Humano (🔴)")
            move = human_player.play(board)
            board.place_piece(move[0], move[1], human_player.player_id)
            print(f"Jugador 1 (🔴) jugó en la posición: ({move[0]}, {move[1]})")
            
            if board.check_connection(human_player.player_id):
                board.print_board()
                print("\n¡Felicitaciones! ¡Has ganado! 🎉")
                break
                
        else:
            print("\nTurno del Jugador AI (🔵)")
            print("AI está pensando...")
            ai_move = ai_player.play(board)
            board.place_piece(ai_move[0], ai_move[1], ai_player.player_id)
            print(f"AI jugó en la posición: ({ai_move[0]}, {ai_move[1]})")
            
            if board.check_connection(ai_player.player_id):
                board.print_board()
                print("\n¡La AI ha ganado! 🤖")
                break
        
        current_turn = (current_turn + 1) % 2

if __name__ == "__main__":
    main()