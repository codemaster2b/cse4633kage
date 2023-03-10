import copy


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
        self.winner = 0
        self.playerOneKing = [7, 7]
        self.playerTwoKing = [9, 9]

        self.board[self.playerOneKing[0]][self.playerOneKing[1]] = 1
        self.board[self.playerTwoKing[0]][self.playerTwoKing[1]] = 2
    
    def validate(self, move):
        if type(move) != type([]) or len(move) != 3 or type(move[1]) != type(1) or type(move[2]) != type(1):
            return False        
        elif move[0] == "W" and self.board[move[1]][move[2]] > 0:
            return False
        elif move[0] == "K" and self.isPlayerOne and abs(self.playerOneKing[0] - move[1]) + abs(self.playerOneKing[1] - move[2]) != 2:
            return False
        elif move[0] == "K" and not self.isPlayerOne and abs(self.playerTwoKing[0] - move[1]) + abs(self.playerTwoKing[1] - move[2]) != 2:
            return False
        elif move[0] == "K" and self.isPlayerOne and move[1] == self.playerTwoKing[0] and move[2] == self.playerTwoKing[1]:
            return False
        elif move[0] == "K" and not self.isPlayerOne and move[1] == self.playerOneKing[0] and move[2] == self.playerOneKing[1]:
            return False
        else:
            return True
    
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

            oneKaged = self.is_kaged(self.playerOneKing)
            twoKaged = self.is_kaged(self.playerTwoKing)

            if self.isPlayerOne and twoKaged:
                self.winner = 1
            elif self.isPlayerOne and oneKaged:
                self.winner = 2
            elif not self.isPlayerOne and oneKaged:
                self.winner = 2
            elif not self.isPlayerOne and twoKaged:
                self.winner = 1

            self.isPlayerOne = not self.isPlayerOne

    def is_kaged(self, position):
        visitedNodes = []
        discoveredNodes = [position]

        isKaged = True
        while isKaged and len(discoveredNodes) > 0:
            node = discoveredNodes.pop(0)
            visitedNodes.append(node)

            leftWall = False
            x = node[0]
            y = node[1]
            while not leftWall and x > 0 and y > 0 and x < self.boardColumns and y < self.boardRows:
                leftWall |= self.board[x-1][y] > 0
                x -= 2

            rightWall = False
            x = node[0]
            y = node[1]
            while not rightWall and x > 0 and y > 0 and x < self.boardColumns and y < self.boardRows:
                rightWall |= self.board[x+1][y] > 0
                x += 2

            upWall = False
            x = node[0]
            y = node[1]
            while not upWall and x > 0 and y > 0 and x < self.boardColumns and y < self.boardRows:
                upWall |= self.board[x][y-1] > 0
                y += 2

            downWall = False
            x = node[0]
            y = node[1]
            while not downWall and x > 0 and y > 0 and x < self.boardColumns and y < self.boardRows:
                downWall |= self.board[x][y+1] > 0
                y += 2
            
            if leftWall and rightWall and upWall and downWall:
                x = node[0]
                y = node[1]
                if self.board[x-1][y] == 0 and not [x-2,y] in discoveredNodes and not [x-2,y] in visitedNodes:
                    discoveredNodes.append([x-2,y])
                if self.board[x+1][y] == 0 and not [x+2,y] in discoveredNodes and not [x+2,y] in visitedNodes:
                    discoveredNodes.append([x+2,y])
                if self.board[x][y-1] == 0 and not [x,y-2] in discoveredNodes and not [x,y-2] in visitedNodes:
                    discoveredNodes.append([x,y-2])
                if self.board[x][y+1] == 0 and not [x,y+2] in discoveredNodes and not [x,y+2] in visitedNodes:
                    discoveredNodes.append([x,y+2])
            else:
                isKaged = False

        return isKaged

