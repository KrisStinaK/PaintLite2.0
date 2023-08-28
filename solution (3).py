import sys

from PyQt5 import uic
from PIL import Image
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from pill2 import Ui_MainWindow


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('pill2.ui', self)

        filename = QFileDialog.getOpenFileName(self, 'Выберите картинку', '')[0]
        img = QPixmap(filename)
        self.label.setPixmap(img)

        self.original = Image.open(filename)
        self.current = Image.open(filename)

        self.pushButton.clicked.connect(self.process)
        self.pushButton_2.clicked.connect(self.process)
        self.pushButton_3.clicked.connect(self.process)
        self.pushButton_4.clicked.connect(self.process)
        self.pushButton_5.clicked.connect(self.rotate)
        self.pushButton_6.clicked.connect(self.rotate)

        self.rotation = 0

    def process(self):
        self.current = self.original.copy()
        self.current = self.current.rotate(self.rotation)
        pixels = self.current.load()
        x, y = self.current.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                if self.sender().text() == 'R':
                    pixels[i, j] = r, 0, 0
                if self.sender().text() == 'G':
                    pixels[i, j] = 0, g, 0
                if self.sender().text() == 'B':
                    pixels[i, j] = 0, 0, b
        self.current.save('current.png')
        self.label.setPixmap(QPixmap('current.png'))



    def rotate(self):
        if self.sender() is self.pushButton_5:
            self.rotation += 90
            self.current = self.current.rotate(90)
        if self.sender() is self.pushButton_6:
            self.rotation -= 90
            self.current = self.current.rotate(-90)
        self.current.save('current.png')
        self.label.setPixmap(QPixmap('current.png'))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())