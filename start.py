# code started from https://github.com/pythonguis/15-minute-apps/blob/master/minesweeper/minesweeper.py with MIT license

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import math
import engine

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.engine = engine.Engine()

        self.playerOneBox = QGroupBox("Player 1")
        self.playerOneBox.width = 300
        self.playerOneBox.height = 200
        playerOneBoxLayout = QGridLayout()
        self.playerOneBox.setLayout(playerOneBoxLayout)

        playerOneAI = QComboBox()
        playerOneAI.addItem("Manual")
        playerOneAI.addItem("Scripted")
        playerOneAI.setCurrentIndex(0)
        playerOneBoxLayout.addWidget(QLabel("AI"),0,0)
        playerOneBoxLayout.addWidget(playerOneAI,0,1)

        self.playerOneMoveLabel = QLabel()
        playerOneBoxLayout.addWidget(QLabel("MOVE"),1,0)
        playerOneBoxLayout.addWidget(self.playerOneMoveLabel,1,1)

        self.playerOneStatusLabel = QLabel()
        playerOneBoxLayout.addWidget(QLabel("STATUS"),2,0)
        playerOneBoxLayout.addWidget(self.playerOneStatusLabel,2,1)

        playerOneAutoCheckBox = QCheckBox("AUTO")
        playerOneBoxLayout.addWidget(playerOneAutoCheckBox,3,0)
        playerOneConfirmButton = QPushButton("CONFIRM")
        playerOneBoxLayout.addWidget(playerOneConfirmButton,3,1)

        self.playerTwoBox = QGroupBox("Player 2")    
        self.playerTwoBox.width = 300
        self.playerTwoBox.height = 200
        playerTwoBoxLayout = QGridLayout()
        self.playerTwoBox.setLayout(playerTwoBoxLayout)

        playerTwoAI = QComboBox()
        playerTwoAI.addItem("Manual")
        playerTwoAI.addItem("Scripted")
        playerTwoAI.setCurrentIndex(0)
        playerTwoBoxLayout.addWidget(QLabel("AI"),0,0)
        playerTwoBoxLayout.addWidget(playerTwoAI,0,1)

        self.playerTwoMoveLabel = QLabel()
        playerTwoBoxLayout.addWidget(QLabel("MOVE"),1,0)
        playerTwoBoxLayout.addWidget(self.playerTwoMoveLabel,1,1)

        self.playerTwoStatusLabel = QLabel()
        playerTwoBoxLayout.addWidget(QLabel("STATUS"),2,0)
        playerTwoBoxLayout.addWidget(self.playerTwoStatusLabel,2,1)

        playerTwoAutoCheckBox = QCheckBox("AUTO")
        playerTwoBoxLayout.addWidget(playerTwoAutoCheckBox,3,0)
        playerTwoConfirmButton = QPushButton("CONFIRM")
        playerTwoBoxLayout.addWidget(playerTwoConfirmButton,3,1)

        playerOneConfirmButton.clicked.connect(self.playerOneConfirmButton_clicked)
        playerTwoConfirmButton.clicked.connect(self.playerTwoConfirmButton_clicked)

        self.boardLayout = QGridLayout()
        self.boardLayout.setSpacing(1)

        self.movesText = QTextEdit()
        self.movesText.width = 200

        forwardBackwardButtonLayout = QHBoxLayout()
        forwardBackwardButtonLayout.addSpacing(10)
        forwardBackwardButtonLayout.addWidget(QLabel("<<"),alignment=Qt.AlignCenter)
        forwardBackwardButtonLayout.addWidget(QLabel("<"),alignment=Qt.AlignCenter)
        forwardBackwardButtonLayout.addWidget(QLabel("______"),alignment=Qt.AlignCenter)
        forwardBackwardButtonLayout.addWidget(QLabel(">"),alignment=Qt.AlignCenter)
        forwardBackwardButtonLayout.addWidget(QLabel(">>"),alignment=Qt.AlignCenter)
        forwardBackwardButtonLayout.addSpacing(10)

        hLayout = QHBoxLayout()
        hLayout.addSpacing(10)
        hLayout.addLayout(self.boardLayout)
        hLayout.addSpacing(10)

        vLayout1 = QVBoxLayout()
        vLayout1.addSpacing(10)
        vLayout1.addLayout(hLayout)
        vLayout1.addSpacing(10)
        vLayout1.addLayout(forwardBackwardButtonLayout)
        vLayout1.addSpacing(10)

        vLayout2 = QVBoxLayout()
        vLayout2.addSpacing(10)
        vLayout2.addWidget(QLabel("Moves Made"))
        vLayout2.addWidget(self.movesText)
        vLayout2.addSpacing(40)

        hLayoutTop = QHBoxLayout()
        hLayoutTop.addSpacing(20)
        hLayoutTop.addWidget(self.playerOneBox)
        hLayoutTop.addSpacing(20)
        hLayoutTop.addWidget(self.playerTwoBox)
        hLayoutTop.addSpacing(20)

        hLayoutBottom = QHBoxLayout()
        hLayoutBottom.addLayout(vLayout1)
        hLayoutBottom.addSpacing(20)
        hLayoutBottom.addLayout(vLayout2)
        hLayoutBottom.addSpacing(20)
        layout = QVBoxLayout()
        layout.addLayout(hLayoutTop)
        layout.addSpacing(10)
        layout.addLayout(hLayoutBottom)
        cw = QWidget()
        cw.setLayout(layout)
        self.setCentralWidget(cw)

        self.init_map()
        self.refresh()
        self.show()

    def get_move(self, moveString):
        text = moveString.replace("(","").replace(")","").replace("'","").replace(" ","")
        split = text.split(",")
        if len(split) == 3:
            split[1] = int(split[1])
            split[2] = int(split[2])
            return split
        else:
            return ("N",0,0)

    def log_text(self, text):
        self.movesText.append(text)

    def playerOneConfirmButton_clicked(self):
        if self.engine.winner == 0 and self.engine.isPlayerOne:
            move = self.get_move(self.playerOneMoveLabel.text())
            self.engine.make_move(move)
            self.refresh()

    def playerTwoConfirmButton_clicked(self):
        if self.engine.winner == 0 and not self.engine.isPlayerOne:
            move = self.get_move(self.playerTwoMoveLabel.text())
            self.engine.make_move(move)
            self.refresh()

    def set_player_move(self, moveString):
        move = self.get_move(moveString)
        valid = self.engine.validate(move)
        if self.engine.isPlayerOne:
            self.playerOneMoveLabel.setText(moveString)
            self.playerOneStatusLabel.setText(str(valid))
        else:
            self.playerTwoMoveLabel.setText(moveString)
            self.playerTwoStatusLabel.setText(str(valid))

    def init_map(self):
        # Add positions to the map
        for x in range(self.engine.boardColumns):
            for y in range(self.engine.boardRows):
                if x % 2 != 0 or y % 2 != 0:
                    item_w = 30
                    item_h = 30

                    w = QPushButton("")
                    w.text = str(x) + "," + str(y)
                    pos = self.get_piece_at(w.text)
                    if pos[0] == "W":
                        if pos[1] % 2 == 0:
                            item_h = 8
                        if pos[2] % 2 == 0:
                            item_w = 8

                    w.setFixedSize(QSize(item_w, item_h))
                    w.clicked.connect(self.board_clicked)
                    self.boardLayout.addWidget(w, y, x)

    def refresh(self):
        if self.engine.winner > 0:
            self.log_text("Player " + str(self.engine.winner) + " won!")
            self.playerOneBox.setStyleSheet("none")
            self.playerTwoBox.setStyleSheet("none")
        elif self.engine.isPlayerOne:
            self.playerOneBox.setStyleSheet("font-weight: bold")
            self.playerTwoBox.setStyleSheet("none")
        else:
            self.playerOneBox.setStyleSheet("none")
            self.playerTwoBox.setStyleSheet("font-weight: bold")

        for x in range(self.engine.boardColumns):
            for y in range(self.engine.boardRows):
                if x % 2 != 0 or y % 2 != 0:
                    w = self.boardLayout.itemAtPosition(y, x).widget()
                    pos = self.get_piece_at(w.text)
                    if pos[0] == "K":
                        if pos[1] % 4 - pos[2] % 4 == 0:
                            w.setStyleSheet("background: tan")
                        else:
                            w.setStyleSheet("background: brown")

                        if self.engine.board[pos[1]][pos[2]] == 1:
                            w.setText("K 1")
                        elif self.engine.board[pos[1]][pos[2]] == 2:
                            w.setText("K 2")
                        else:
                            w.setText("")
                    elif pos[0] == "W":
                        if self.engine.board[pos[1]][pos[2]] > 0:
                            w.setStyleSheet("background: green")
                        else:
                            w.setStyleSheet("background: black")


    def board_clicked(self):
        pos = self.get_piece_at(self.sender().text)
        self.log_text(str(pos))
        self.set_player_move(str(pos))

    def get_piece_at(self, positionStr):
        pos = positionStr.split(",")
        y = int(pos[0])
        x = int(pos[1])

        piece = "K"
        if x % 2 == 0 and y % 2 == 0:
            piece = "No"
        elif x % 2 == 0 or y % 2 == 0:
            piece = "W"
        
        return piece, x, y

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec_()