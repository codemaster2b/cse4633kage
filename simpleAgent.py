
import engine


class SimpleAgent:

    def __init__(self) -> None:
        pass

    # engine is a copy of the current game state
    #
    # returns a list/sequence of 3 items like ("W",5,7)
    # the first element is "K" for king or "W" for wall
    # the last two elements are integers in range(17)
    def move(self, gameState: engine.Engine) -> list:
        move = ("K",1,1)
        target = gameState.playerOneKing
        if gameState.isPlayerOne:
            target = gameState.playerTwoKing
           
        if gameState.board[target[0]-1][target[1]] == 0:
            move = ("W",target[0]-1,target[1])
        elif gameState.board[target[0]][target[1]-1] == 0:
            move = ("W",target[0],target[1]-1)
        elif gameState.board[target[0]+1][target[1]] == 0:
            move = ("W",target[0]+1,target[1])
        elif gameState.board[target[0]][target[1]+1] == 0:
            move = ("W",target[0],target[1]+1)

        return move