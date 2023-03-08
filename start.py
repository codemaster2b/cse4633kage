# code started from https://github.com/pythonguis/15-minute-apps/blob/master/minesweeper/minesweeper.py with MIT license

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import random
import time

class Pos(QWidget):
    expandable = pyqtSignal(int, int)
    clicked = pyqtSignal()
    ohno = pyqtSignal()

    def __init__(self, x, y, *args, **kwargs):
        super(Pos, self).__init__(*args, **kwargs)

        self.setFixedSize(QSize(20, 20))

        self.x = x
        self.y = y

    def reset(self):
        self.is_start = False
        self.is_mine = False
        self.adjacent_n = 0

        self.is_revealed = False
        self.is_flagged = False

        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        r = event.rect()

        if self.is_revealed:
            color = self.palette().color(QPalette.Background)
            outer, inner = color, color
        else:
            outer, inner = Qt.gray, Qt.lightGray

        p.fillRect(r, QBrush(inner))
        pen = QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)
        p.drawPixmap(r, QPixmap(QImage("./images/bug.png")))
        pen = QPen("blue")
        p.setPen(pen)
        f = p.font()
        f.setBold(True)
        p.setFont(f)
        p.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, str(self.adjacent_n))

    def flag(self):
        self.is_flagged = True
        self.update()

        self.clicked.emit()

    def reveal(self):
        self.is_revealed = True
        self.update()

    def click(self):
        if not self.is_revealed:
            self.reveal()
            if self.adjacent_n == 0:
                self.expandable.emit(self.x, self.y)

        self.clicked.emit()

    def mouseReleaseEvent(self, e):

        if (e.button() == Qt.RightButton and not self.is_revealed):
            self.flag()

        elif (e.button() == Qt.LeftButton):
            self.click()

            if self.is_mine:
                self.ohno.emit()


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

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

        playerOneMoveLabel = QLabel()
        playerOneBoxLayout.addWidget(QLabel("MOVE"),1,0)
        playerOneBoxLayout.addWidget(playerOneMoveLabel,1,1)

        playerOneStatusLabel = QLabel()
        playerOneBoxLayout.addWidget(QLabel("STATUS"),2,0)
        playerOneBoxLayout.addWidget(playerOneStatusLabel,2,1)

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

        playerTwoMoveLabel = QLabel()
        playerTwoBoxLayout.addWidget(QLabel("MOVE"),1,0)
        playerTwoBoxLayout.addWidget(playerTwoMoveLabel,1,1)

        playerTwoStatusLabel = QLabel()
        playerTwoBoxLayout.addWidget(QLabel("STATUS"),2,0)
        playerTwoBoxLayout.addWidget(playerTwoStatusLabel,2,1)

        playerTwoAutoCheckBox = QCheckBox("AUTO")
        playerTwoBoxLayout.addWidget(playerTwoAutoCheckBox,3,0)
        playerTwoConfirmButton = QPushButton("CONFIRM")
        playerTwoBoxLayout.addWidget(playerTwoConfirmButton,3,1)

        playerOneConfirmButton.clicked.connect(self.playerOneConfirmButton_clicked)
        playerTwoConfirmButton.clicked.connect(self.playerTwoConfirmButton_clicked)
        self.set_player(True)

        self.boardLayout = QGridLayout()
        self.boardLayout.setSpacing(1)

        movesText = QTextEdit()
        movesText.width = 200

        cursor = QTextCursor(movesText.document())
        cursor.setPosition(0)
        movesText.setTextCursor(cursor)
        movesText.insertPlainText('Your Move Mate')

       
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
        vLayout2.addWidget(movesText)
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
        self.reset_map()
        self.show()


    def playerOneConfirmButton_clicked(self):
        self.set_player(False)
        return

    def playerTwoConfirmButton_clicked(self):
        self.set_player(True)
        return

    def set_player(self, isPlayerOne):
        if isPlayerOne:
            self.playerOneBox.setStyleSheet("font-weight: bold")
            self.playerTwoBox.setStyleSheet("none")
        else:
            self.playerTwoBox.setStyleSheet("font-weight: bold")
            self.playerOneBox.setStyleSheet("none")

    def init_map(self):
        # Add positions to the map
        for x in range(17):
            for y in range(17):
                w = QPushButton("")
                w.setStyleSheet("background: white")
                item_w = 30
                if x % 2 == 0:
                    item_w = 8

                item_h = 30
                if y % 2 == 0:
                    item_h = 8

                if x % 2 != 0 and y % 2 != 0:
                    if x % 4 - y % 4 == 0:
                        w.setStyleSheet("background: tan")
                    else:
                        w.setStyleSheet("background: brown")
                else:
                    w.setStyleSheet("background: black")


                if x % 2 != 0 or y % 2 != 0:
                    w.setFixedSize(QSize(item_w, item_h))
                    self.boardLayout.addWidget(w, y, x)

                # Connect signal to handle expansion.
                #w.clicked.connect(self.trigger_start)
                #w.expandable.connect(self.expand_reveal)
                #w.ohno.connect(self.game_over)

    def reset_map(self):
        # Clear all mine positions
        #for x in range(0, 8):
            #for y in range(0, 8):
                #w = self.boardLayout.itemAtPosition(y, x).widget()
                #w.reset()
        return

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec_()