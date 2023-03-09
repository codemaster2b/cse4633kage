class Engine:

    def __init__(self):
        self.board = []
        self.boardRows = 17
        self.boardColumns = 17
        for i in range(self.boardRows):
            self.board.append([])
            for j in range(self.boardColumns):
                self.board[i].append(0)
        
        self.isPlayerOne = True
        self.playerOneKing = [7, 7]
        self.playerTwoKing = [9, 9]

        self.board[6][7] = 1
        self.board[8][7] = 1
        self.board[7][6] = 1
        self.board[7][8] = 1

        self.board[self.playerOneKing[0]][self.playerOneKing[1]] = 1
        self.board[self.playerTwoKing[0]][self.playerTwoKing[1]] = 2
    
    def validate(self, move):
        if type(move) == type([]) and len(move) == 3 and type(move[1]) == type(1) and type(move[2]) == type(1):
            return True
        else:
            return False
    
    def make_move(self, move):
        if self.validate(move):
            if move[0] == "K":
                if self.isPlayerOne:
                    self.board[self.playerOneKing[0]][self.playerOneKing[1]] = 0
                    self.playerOneKing[0] = move[1]
                    self.playerOneKing[1] = move[2]
                    self.board[self.playerOneKing[0]][self.playerOneKing[1]] = 1
                else:
                    self.board[self.playerTwoKing[0]][self.playerTwoKing[1]] = 0
                    self.playerTwoKing[0] = move[1]
                    self.playerTwoKing[1] = move[2]
                    self.board[self.playerTwoKing[0]][self.playerTwoKing[1]] = 2
            elif move[0] == "W":
                self.board[move[1]][move[2]] = 1

            self.isPlayerOne = not self.isPlayerOne

