class Engine:

    Board = []
    BoardRows = 8
    BoardColumns = 8

    def __init__(self):
        self.Board = []
        for i in range(self.BoardRows):
            self.Board.append([])
            for j in range(self.BoardColumns):
                self.Board[i].append(1)

