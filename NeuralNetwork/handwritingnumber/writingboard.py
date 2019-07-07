from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, \
                            QMessageBox, QAction, qApp, QMenu, \
                            QGridLayout, QLabel, QRadioButton
from PyQt5.QtGui import QPainter, QPen, QIcon, QFont, QPixmap, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QPoint, QSize
from test import get_trained_network
import numpy as np
import sys
import os

BASE_DIR = os.path.dirname(__file__)
ICON_MAIN = 'main.jpg'
ICON_QUIT = 'quit.jpg'
ICON_EXIT = 'exit.jpg'

class DrawArea(QWidget):
    
    def __init__(self, parent = None,
                 size = QSize(140, 140),
                 pencolor = Qt.black,
                 backcolor = Qt.white,
                 pensize = 5,
                 erasemode = False):
        super(DrawArea, self).__init__()

        # Do not track the mouse while moving without pressing
        self.setMouseTracking(False)

        # Arguments
        self.size = size
        self.pencolor = pencolor
        self.eraserstate = erasemode
        self.backcolor = backcolor
        self.pensize = pensize

        # Painter
        self.painter = QPainter()

        # Pixmap
        self.pixmap = QPixmap(self.size)
        self.pixmap.fill()

        # Position label
        self.label = QLabel('', self)

        # Position
        self.curr_pos = QPoint(0, 0)
        self.last_pos = QPoint(0, 0)

    # Events
    def paintEvent(self, event):
        self.painter.begin(self)
        self.painter.drawPixmap(0, 0, self.pixmap)
        self.painter.end()

    def mousePressEvent(self, event):
        self.curr_pos = event.pos()
        self.last_pos = self.curr_pos
        self.label.setText('X: {}, Y: {}'.format(self.curr_pos.x(), self.curr_pos.y()))
        self.label.show()

    def mouseReleaseEvent(self, event):
        self.label.hide()

    def mouseMoveEvent(self, event):
        self.curr_pos = event.pos()

        self.painter.begin(self.pixmap)
        if self.eraserstate:
            pen = QPen(self.backcolor, 15, Qt.SolidLine)
        else:
            pen = QPen(self.pencolor, self.pensize, Qt.SolidLine)
        self.painter.setPen(pen)
        self.painter.drawLine(self.last_pos, self.curr_pos)
        self.painter.end()

        self.label.setText('X:{} Y:{}'.format(self.curr_pos.x(), self.curr_pos.y()))
        
        self.last_pos = self.curr_pos
        self.update()

    # API
    def clearArea(self):
        self.pixmap.fill()
        self.update()

    def changePenColor(self, color):
        self.pencolor = color

    def changePenSize(self, size):
        self.pensize = size

    def changeBackColor(self, color):
        self.backcolor = color

    def changeEraserState(self, change_to = None):
        if change_to:
            self.eraserstate = change_to
        else:    
            self.eraserstate = not self.eraserstate

    def getImage(self):
        return self.pixmap.toImage()

class PaintBoard(QWidget):

    def __init__(self, parent = None):
        print ('Paint board initializing...')
        super(PaintBoard, self).__init__()

        # Neural network
        self.net = get_trained_network()

        # Window
        self.setGeometry(100, 100, 280, 210)
        self.setWindowTitle('Handwriting Number Identify')
        self.setWindowIcon(QIcon(os.path.join(BASE_DIR, ICON_MAIN)))

        # Layout
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Draw Area
        self.drawarea = DrawArea(self)
        self.layout.addWidget(self.drawarea, 0, 0, 4, 3)

        # Button
        btn_identify = QPushButton('Identify')
        btn_identify.setToolTip('Start to identify your handwriting number!')
        btn_identify.clicked.connect(self.identifyImage)
        self.layout.addWidget(btn_identify, 0, 4)

        btn_clear = QPushButton('Clear')
        btn_clear.setToolTip('Clear the paint board')
        btn_clear.clicked.connect(self.drawarea.clearArea)
        self.layout.addWidget(btn_clear, 1, 4)

        btn_eraser = QRadioButton('Eraser')
        btn_eraser.setToolTip('Select eraser tool')
        btn_eraser.setChecked(False)
        btn_eraser.toggled.connect(lambda: self.checkEraseMode(btn_eraser))
        self.layout.addWidget(btn_eraser, 2, 4)

         # Label
        self.label = QLabel('')
        self.layout.addWidget(self.label, 3, 4)

    def identifyImage(self):
        image = self.drawarea.getImage().scaled(28, 28)
        input_data = list()
        print(image.pixel(0, 0))
        for x in range(28):
            for y in range(28):
                if image.pixel(x, y) == 4278190080:
                    input_data.append(255)
                else: 
                    input_data.append(0)
        
        input_data = np.asfarray(input_data) / 255 * 0.99 + 0.01
        print(input_data.reshape(28, 28))
        output_data = self.net.query(input_data)
        output_number = output_data.argmax()
        self.label.setText('Number: {}'.format(output_number))

    def checkEraseMode(self, btn):
        self.drawarea.changeEraserState(btn.isChecked())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pyqt = PaintBoard()
    pyqt.show()
    app.exec_()
    
