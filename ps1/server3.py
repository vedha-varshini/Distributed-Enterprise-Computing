import socket
import threading

# Game session class
class TicTacToeSession(threading.Thread):
    def __init__(self, player1, player2):
        threading.Thread.__init__(self)
        self.player1 = player1
        self.player2 = player2
        self.board = [' ']*9
        self.current_turn = self.player1
        self.player_tokens = {self.player1: 'X', self.player2: 'O'}
    
    def run(self):
        self.player1.send("You are Player 1 (X)".encode('utf-8'))
        self.player2.send("You are Player 2 (O)".encode('utf-8'))
        
        while True:
            self.current_turn.send("Your move (enter position 1-9): ".encode('utf-8'))
            position = int(self.current_turn.recv(1024).decode('utf-8')) - 1
            if self.board[position] == ' ':
                self.board[position] = self.player_tokens[self.current_turn]
                self.current_turn = self.player2 if self.current_turn == self.player1 else self.player1
                self.broadcast_board()
                if self.check_winner():
                    winner = self.player1 if self.current_turn == self.player2 else self.player2
                    winner.send("You win!".encode('utf-8'))
                    break
                elif ' ' not in self.board:
                    self.broadcast("It's a draw!")
                    break
    
    def broadcast_board(self):
        board_str = f"{self.board[0]}|{self.board[1]}|{self.board[2]}\n" \
                    f"{self.board[3]}|{self.board[4]}|{self.board[5]}\n" \
                    f"{self.board[6]}|{self.board[7]}|{self.board[8]}"
        self.player1.send(board_str.encode('utf-8'))
        self.player2.send(board_str.encode('utf-8'))
    
    def broadcast(self, message):
        self.player1.send(message.encode('utf-8'))
        self.player2.send(message.encode('utf-8'))
    
    def check_winner(self):
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6)]
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != ' ':
                return True
        return False

# Main server code
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 5555))
server.listen(5)

print("Server started, waiting for connections...")

players = []

while True:
    client_socket, addr = server.accept()
    print(f"New connection from {addr}")
    players.append(client_socket)
    if len(players) == 2:
        session = TicTacToeSession(players[0], players[1])
        session.start()
        players = []

