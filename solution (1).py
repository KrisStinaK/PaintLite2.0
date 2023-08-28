import sys

from PyQt5.QtGui import QPainter, QPen, QImage
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QFileDialog
from PyQt5.QtCore import Qt, QLineF, QRectF, QPointF


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 600, 600)

        mainMenu = self.menuBar()
        instmenu = mainMenu.addMenu("Инстументы")
        colormenu = mainMenu.addMenu("Цвет")
        sizemanu = mainMenu.addMenu("Толщина")
        file = mainMenu.addMenu("Файл")

        brush = QAction("Кисть", self)
        instmenu.addAction(brush)
        brush.triggered.connect(self.setBrush)

        line = QAction("Линия", self)
        instmenu.addAction(line)
        line.triggered.connect(self.setLine)

        circle = QAction("Круг", self)
        instmenu.addAction(circle)
        circle.triggered.connect(self.setCircle)

        rect = QAction("Прямоугольник", self)
        instmenu.addAction(rect)
        rect.triggered.connect(self.setRectangle)

        red = QAction("Красный", self)
        colormenu.addAction(red)
        red.triggered.connect(self.redColor)

        blue = QAction("Синий", self)
        colormenu.addAction(blue)
        blue.triggered.connect(self.blueColor)

        yellow = QAction("Желтый", self)
        colormenu.addAction(yellow)
        yellow.triggered.connect(self.yellowColor)

        black = QAction("Черный", self)
        colormenu.addAction(black)
        black.triggered.connect(self.blackColor)

        fpx = QAction("4", self)
        sizemanu.addAction(fpx)
        fpx.triggered.connect(self.four)

        epx = QAction("8", self)
        sizemanu.addAction(epx)
        epx.triggered.connect(self.eight)

        sipx = QAction("16", self)
        sizemanu.addAction(sipx)
        sipx.triggered.connect(self.sixteen)

        thpx = QAction("32", self)
        sizemanu.addAction(thpx)
        thpx.triggered.connect(self.thirtytwo)

        get = QAction('Вставить фото', self)
        file.addAction(get)
        get.triggered.connect(self.getImage)

        delete = QAction('Очистить', self)
        file.addAction(delete)
        delete.triggered.connect(self.deleteImage)

        self.image_foreground = QImage(self.size(), QImage.Format_ARGB32)
        self.image_foreground.fill(Qt.transparent)

        self.instrument = 'brush'

        self.brushColor = Qt.black
        self.brushSize = 8

        self.start_pos = QPointF()
        self.end_pos = QPointF()

        self.objects = []

    def getImage(self):
        filename = QFileDialog.getOpenFileName(
            self, "", "",
            "Images(*.png *.jpg *.jpeg);;PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*)"
        )[0]
        if not filename:
            return
        self.image_foreground.load(filename)

    def deleteImage(self):
        self.image_foreground.fill(Qt.white)
        self.update()

    def draw(self, canvas):
        painter = QPainter(canvas)
        painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine))

        if self.instrument == 'brush':
            for p in self.objects:
                painter.drawPoint(p)

        elif self.instrument == 'line':
            painter.drawLine(self.start_pos, self.end_pos)

        elif self.instrument == 'circle':
            painter.drawEllipse(QRectF(self.start_pos, self.end_pos))

        elif self.instrument == 'rectangle':
            painter.drawRect(QRectF(self.start_pos, self.end_pos))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.image_foreground.rect(), self.image_foreground)

        # Рисуем на виджете
        self.draw(self)

    def mousePressEvent(self, event):
        self.start_pos = event.pos()
        self.objects.clear()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.end_pos = event.pos()
            self.objects.append(self.end_pos)

            self.update()

    def mouseReleaseEvent(self, event):
        self.end_pos = event.pos()
        self.objects.append(self.end_pos)

        # При отпускании кнопки мышки рисуем на картинке
        self.draw(self.image_foreground)
        self.update()

    def setBrush(self):
        self.instrument = 'brush'

    def setLine(self):
        self.instrument = 'line'

    def setCircle(self):
        self.instrument = 'circle'

    def setRectangle(self):
        self.instrument = 'rectangle'

    def four(self):
        self.brushSize = 4

    def eight(self):
        self.brushSize = 8

    def sixteen(self):
        self.brushSize = 16

    def thirtytwo(self):
        self.brushSize = 32

    def blackColor(self):
        self.brushColor = Qt.black

    def redColor(self):
        self.brushColor = Qt.red

    def blueColor(self):
        self.brushColor = Qt.blue

    def yellowColor(self):
        self.brushColor = Qt.yellow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = Window()
    wnd.show()
    sys.exit(app.exec())