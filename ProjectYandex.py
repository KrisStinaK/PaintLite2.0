from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PIL import Image, ImageFilter
import sys


class Brushpoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, painter):
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.setPen(QColor(0, 0, 0))
        painter.drawEllipse(self.x - 5, self.y - 5, 10, 10)


class Line:
    def __init__(self, sx, sy, ex, ey):
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey

    def draw(self, painter):
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.setPen(QColor(0, 0, 0))
        painter.drawLine(self.sx, self.sy, self.ex, self.ey)


class Circle:
    def __init__(self, cx, cy, x, y):
        self.cx = cx
        self.cy = cy
        self.x = x
        self.y = y

    def draw(self, painter):
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.setPen(QColor(0, 0, 0))
        radius = int(((self.cx - self.x) ** 2 + (self.cy - self.y) ** 2) ** 0.5)
        painter.drawEllipse(self.cx - radius, self.cy - radius, 2 * radius, 2 * radius)


class Canvas(QWidget):
    def __init__(self):
        super(Canvas, self).__init__()

        self.objects = []
        self.instrument = 'brush'

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        for obj in self.objects:
            obj.draw(painter)
        painter.end()

    def setBrush(self):
        self.instrument = 'brush'

    def setLine(self):
        self.instrument = 'line'

    def setCircle(self):
        self.instrument = 'circle'

    def mousePressEvent(self, event):
        if self.instrument == 'brush':
            self.objects.append(Brushpoint(event.x(), event.y()))
            self.update()
        elif self.instrument == 'line':
            self.objects.append(Line(event.x(), event.y(), event.x(), event.y()))
            self.update()
        elif self.instrument == 'circle':
            self.objects.append(Circle(event.x(), event.y(), event.x(), event.y()))
            self.update()

    def mouseMoveEvent(self, event):
        if self.instrument == 'brush':
            self.objects.append(Brushpoint(event.x(), event.y()))
            self.update()
        elif self.instrument == 'line':
            self.objects[-1].ex = event.x()
            self.objects[-1].ey = event.y()
            self.update()
        elif self.instrument == 'circle':
            self.objects[-1].x = event.x()
            self.objects[-1].y = event.y()
            self.update()


class Window(QMainWindow, Canvas):
    def __init__(self):
        super().__init__()

        self.setCentralWidget(Canvas())

        self.setWindowTitle("Крутой Paint")
        self.setGeometry(100, 100, 800, 600)
        self.resize(1000, 800)

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.lastPoint = QPoint()
        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.black
        self.brushColor2 = Qt.black
        self.brushline = Qt.SolidLine
        self.textsize = 2
        self.lastic = Qt.white
        self.p = QPlainTextEdit(self)
        self.p.resize(1000, 800)
        self.p.move(0, 21)
        self.p.hide()

        self.button = QPushButton(self)
        self.button.resize(20, 20)
        self.button.move(950, 35)

        self.button1 = QPushButton(self)
        self.button1.resize(20, 20)
        self.button1.move(950, 60)

        self.button2 = QPushButton(self)
        self.button2.resize(20, 20)
        self.button2.move(950, 84)

        self.label = QLabel('Цвет кисти', self)
        self.label.resize(86, 15)
        self.label.move(850, 38)

        self.label_ = QLabel('Цвет заливки', self)
        self.label_.resize(86, 15)
        self.label_.move(850, 63)

        self.label_1 = QLabel('Цвет текста', self)
        self.label_1.resize(86, 15)
        self.label_1.move(850, 87)

        self.label2 = QLabel(self)
        self.label2.hide()

        # объект для рисования
        self.lastPoint = QPoint()
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("Файл")
        b_canvas = mainMenu.addMenu("Холст")
        b_fill = mainMenu.addMenu("Заливка")
        b_b = mainMenu.addMenu("Кисть")
        b_figur = mainMenu.addMenu("Фигуры")
        b_size = mainMenu.addMenu("Размер кисти")
        b_text = mainMenu.addMenu("Текст")
        b_foto = mainMenu.addMenu("Вставить фото")
        b_eff = mainMenu.addMenu("Фильтры")

        saveAction = QAction("Сохранить", self)
        saveAction.setShortcut("Ctrl + S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)

        clearAction = QAction("Очистить холст", self)
        clearAction.setShortcut("Ctrl + C")
        b_canvas.addAction(clearAction)
        clearAction.triggered.connect(self.clear)

        draw = QAction("Рисовать", self)
        b_canvas.addAction(draw)
        draw.triggered.connect(self.Draw)

        drawfigur = QAction("Круг", self)
        b_figur.addAction(drawfigur)
        drawfigur.triggered.connect(self.centralWidget().setCircle)

        drawfigur2 = QAction("Линия", self)
        b_figur.addAction(drawfigur2)
        drawfigur2.triggered.connect(self.centralWidget().setLine)

        clr = QAction("Залить", self)
        b_fill.addAction(clr)
        clr.triggered.connect(self.Fill)

        color = QAction("Цвет", self)
        b_b.addAction(color)
        color.triggered.connect(self.showColorDialog)

        brush1 = QAction("Стиль_1", self)
        b_b.addAction(brush1)
        brush1.triggered.connect(self.DashLine)

        brush2 = QAction("Стиль_2", self)
        b_b.addAction(brush2)
        brush2.triggered.connect(self.DashDotLine)

        brush3 = QAction("Стиль_3", self)
        b_b.addAction(brush3)
        brush3.triggered.connect(self.DotLine)

        brush4 = QAction("Стиль_4", self)
        b_b.addAction(brush4)
        brush4.triggered.connect(self.DashDotDotLine)

        brush5 = QAction("Обычный стиль", self)
        b_b.addAction(brush5)
        brush5.triggered.connect(self.SolidLine)

        eraser = QAction("Стереть", self)
        b_canvas.addAction(eraser)
        eraser.triggered.connect(self.Eraser)

        text = QAction("Открыть документ", self)
        b_text.addAction(text)
        text.triggered.connect(self.Text)

        text_save = QAction("Сохранить документ", self)
        b_text.addAction(text_save)
        text_save.triggered.connect(self.Text_save)

        textsize = QAction("Шрифт", self)
        b_text.addAction(textsize)
        textsize.triggered.connect(self.getFont)

        textcolor = QAction("Цвет шрифта", self)
        b_text.addAction(textcolor)
        textcolor.triggered.connect(self.fontColor)

        textcolor2 = QAction("Цвет", self)
        b_text.addAction(textcolor2)
        textcolor2.triggered.connect(self.onTextChanged)

        textcolor3 = QAction("Выделить", self)
        b_text.addAction(textcolor3)
        textcolor3.triggered.connect(self.textplaincolor)

        foto = QAction("Вставить фото", self)
        b_foto.addAction(foto)
        foto.triggered.connect(self.Foto)

        self.exitAction = QAction("Выход", self)
        fileMenu.addAction(self.exitAction)
        self.exitAction.triggered.connect(self.close)

        self.fotor = QAction("Повернуть вправо", self)
        b_foto.addAction(self.fotor)
        self.fotor.triggered.connect(self.rotate_right)
        self.fotor.setEnabled(False)

        self.fotol = QAction("Повернуть влево", self)
        b_foto.addAction(self.fotol)
        self.fotol.triggered.connect(self.rotate_45_left)
        self.fotol.setEnabled(False)

        self.fotol2 = QAction("Повернуть на 45 вправо", self)
        b_foto.addAction(self.fotol2)
        self.fotol2.triggered.connect(self.rotate_45_right)
        self.fotol2.setEnabled(False)

        self.fotol3 = QAction("Повернуть на 45 влево", self)
        b_foto.addAction(self.fotol3)
        self.fotol3.triggered.connect(self.rotate_45_left)
        self.fotol3.setEnabled(False)

        self.fotol4 = QAction("Повернуть на 180", self)
        b_foto.addAction(self.fotol4)
        self.fotol4.triggered.connect(self.rotate_180_right)
        self.fotol4.setEnabled(False)

        self.fotodel = QAction("Убрать фото", self)
        b_foto.addAction(self.fotodel)
        self.fotodel.triggered.connect(self.Delfoto)
        self.fotodel.setEnabled(False)

        self.neg = QAction("Негатив", self)
        b_eff.addAction(self.neg)
        self.neg.triggered.connect(self.Negative)
        self.neg.setEnabled(False)

        self.chb = QAction("Черно-белое", self)
        b_eff.addAction(self.chb)
        self.chb.triggered.connect(self.invert)
        self.chb.setEnabled(False)

        self.bbb = QAction("Странная инверсия", self)
        b_eff.addAction(self.bbb)
        self.bbb.triggered.connect(self.curve)
        self.bbb.setEnabled(False)

        self.bbo = QAction("Оригинал", self)
        b_eff.addAction(self.bbo)
        self.bbo.triggered.connect(self.Foto2)
        self.bbo.setEnabled(False)

        self.bbo1 = QAction("Прозрачный цвет", self)
        b_eff.addAction(self.bbo1)
        self.bbo1.triggered.connect(self.Foto2)
        self.bbo1.setEnabled(False)

        # размер кисти
        pix_4 = QAction("4px", self)
        b_size.addAction(pix_4)
        pix_4.triggered.connect(self.Pixel_4)

        pix_7 = QAction("7px", self)
        b_size.addAction(pix_7)
        pix_7.triggered.connect(self.Pixel_7)

        pix_9 = QAction("9px", self)
        b_size.addAction(pix_9)
        pix_9.triggered.connect(self.Pixel_9)

        pix_12 = QAction("12px", self)
        b_size.addAction(pix_12)
        pix_12.triggered.connect(self.Pixel_12)

        pix_15 = QAction("15px", self)
        b_size.addAction(pix_15)
        pix_15.triggered.connect(self.Pixel_15)

        pix_17 = QAction("17px", self)
        b_size.addAction(pix_17)
        pix_17.triggered.connect(self.Pixel_17)

        pix_20 = QAction("20px", self)
        b_size.addAction(pix_20)
        pix_20.triggered.connect(self.Pixel_20)

        pix_25 = QAction("25px", self)
        b_size.addAction(pix_25)
        pix_25.triggered.connect(self.Pixel_25)

        pix_30 = QAction("30px", self)
        b_size.addAction(pix_30)
        pix_30.triggered.connect(self.Pixel_30)

    # клик мышки
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    # отслеживание мышки
    def mouseMoveEvent(self, event):

        if (event.buttons() and Qt.LeftButton) and self.drawing:
            self.painter = QPainter(self.image)
        elif self.instrument == 'Line':
            self.objects[-1].ex = event.x()
            self.objects[-1].ey = event.y()
            self.update()


        # установка ручки
        self.painter.setPen(QPen(self.brushColor, self.brushSize,
                            self.brushline, Qt.RoundCap, Qt.RoundJoin))
        self.painter.drawLine(self.lastPoint, event.pos())
        self.lastPoint = event.pos()
        self.update()


    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    # сохранить
    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if filePath == "":
            return
        self.image.save(filePath)

    # очистка
    def clear(self):
        self.image.fill(Qt.white)
        self.update()

    def Fill(self):
        self.selected_color_fill = QColorDialog.getColor()
        if self.selected_color_fill.isValid():
            self.brushColor_fill = QColor(*self.selected_color_fill.getRgb())
            self.image.fill(QColor(self.brushColor_fill))
            self.update()
            self.button1.setStyleSheet(
                f"background-color: {self.selected_color_fill.name()}")

    def Draw(self):
        self.label2.show()

    # размер кисти
    def Pixel_4(self):
        self.brushSize = 4

    def Pixel_7(self):
        self.brushSize = 7

    def Pixel_9(self):
        self.brushSize = 9

    def Pixel_12(self):
        self.brushSize = 12

    def Pixel_15(self):
        self.brushSize = 15

    def Pixel_17(self):
        self.brushSize = 17

    def Pixel_20(self):
        self.brushSize = 20

    def Pixel_25(self):
        self.brushSize = 25

    def Pixel_30(self):
        self.brushSize = 30


    def showColorDialog(self):
        self.selected_color = QColorDialog.getColor()
        if self.selected_color.isValid():
            self.button.setStyleSheet(
                f"background-color: {self.selected_color.name()}")
            self.brushColor = QColor(*self.selected_color.getRgb())

    def Eraser(self):
        self.brushColor = Qt.white
        self.brushline = Qt.SolidLine

    # line
    def DashLine(self):
        self.brushline = Qt.DashLine

    def DashDotLine(self):
        self.brushline = Qt.DashDotLine

    def DotLine(self):
        self.brushline = Qt.DotLine

    def DashDotDotLine(self):
        self.brushline = Qt.DashDotDotLine

    def SolidLine(self):
        self.brushline = Qt.SolidLine

    def Text(self):
        self.p.show()
        self.Delfoto()

    def Text_save(self):
        file, _ = QFileDialog.getSaveFileName(self, "Save File", "",
                                                  "(*.txt);;")

        if file == "":
            return
        f = open(file, mode='w', encoding='utf8')
        f.write(self.p.toPlainText())
        f.close()

    def fontsize(self):
        font = QFont("Courier", 20)
        QApplication.setFont(font, self.p.toPlainText())

    def getFont(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.p.setFont(font)

    def fontColor(self):
        self.selected_color2 = QColorDialog.getColor()
        if self.selected_color2.isValid():
            Palette = QPalette()
            Palette.setColor(QPalette.Text, self.selected_color2)
            self.p.setPalette(Palette)
            self.button2.setStyleSheet(
                f"background-color: {self.selected_color2.name()}")

    def Foto(self, event):
        self.label2.show()
        self.filename = QFileDialog.getOpenFileName(self, 'Выберите картинку', '')[0]
        self.img = QPixmap(self.filename)
        self.foto_orig = self.img
        self.label2.setPixmap(self.img)
        self.label2.resize(1000, 800)
        self.fotor.setEnabled(True)
        self.fotol.setEnabled(True)
        self.fotodel.setEnabled(True)
        self.neg.setEnabled(True)
        self.chb.setEnabled(True)
        self.bbb.setEnabled(True)
        self.fotol2.setEnabled(True)
        self.fotol3.setEnabled(True)
        self.fotol4.setEnabled(True)
        self.bbo.setEnabled(True)
        self.bbo1.setEnabled(True)

        self.original = Image.open(self.filename)
        self.current = Image.open(self.filename)

        self.rotation = 0

    def Delfoto(self):
        self.label2.hide()
        self.fotor.setEnabled(False)
        self.fotol.setEnabled(False)
        self.fotodel.setEnabled(False)
        self.neg.setEnabled(False)
        self.chb.setEnabled(False)
        self.bbb.setEnabled(False)
        self.fotol2.setEnabled(False)
        self.fotol3.setEnabled(False)
        self.fotol4.setEnabled(False)
        self.bbo.setEnabled(False)

    def Foto2(self):
        self.label2.setPixmap(self.foto_orig)
        self.bbo.setEnabled(True)

    def rotate_right(self):
        self.rotation += 90
        self.current = self.current.rotate(90)
        self.current.save('current.png')
        self.label2.setPixmap(QPixmap('current.png'))

    def rotate2_left(self):
        self.rotation -= 90
        self.current = self.current.rotate(-90)
        self.current.save('current.png')
        self.label2.setPixmap(QPixmap('current.png'))

    def rotate_45_right(self):
        self.rotation += 45
        self.current = self.current.rotate(45)
        self.current.save('current.png')
        self.label2.setPixmap(QPixmap('current.png'))

    def rotate_45_left(self):
        self.rotation -= 45
        self.current = self.current.rotate(-45)
        self.current.save('current.png')
        self.label2.setPixmap(QPixmap('current.png'))

    def rotate_180_right(self):
        self.rotation -= 45
        self.current = self.current.rotate(-180)
        self.current.save('current.png')
        self.label2.setPixmap(QPixmap('current.png'))

    def Negative(self):
        self.current = self.original.copy()
        self.current = self.current.rotate(self.rotation)
        pixels = self.current.load()
        x, y = self.current.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                pixels[i, j] = 255 - r, 255 - g, 255 - b

        self.current.save('current.png')
        self.label2.setPixmap(QPixmap('current.png'))

    def invert(self):
        x, y = self.current.size
        pixels = self.current.load()
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                bw = (r + g + b) // 3
                pixels[i, j] = bw, bw, bw

        self.current.save('current.png')
        self.label2.setPixmap(QPixmap('current.png'))

    def curve(self):
        x, y = self.current.size
        pixels = self.current.load()
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                pixels[i, j] = r, b, g
        self.current.save('current.png')
        self.label2.setPixmap(QPixmap('current.png'))

    def crop_rect(self):
        self.current.crop((50, 50, 50, 50))
        self.current.save('current.png')
        self.label2.setPixmap(QPixmap('current.png'))

    def process(self):
        self.current = self.original.copy()
        self.current = self.current.rotate(self.rotation)
        pixels = self.current.load()
        x, y = self.current.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                pixels[i, j] = r, 0, 0
        self.current.save('current.png')
        self.label.setPixmap(QPixmap('current.png'))

    def onTextChanged(self):
        self.selected_color7 = QColorDialog.getColor()
        if self.selected_color7.isValid():
            self.p.setStyleSheet(
                f"background-color: {self.selected_color7.name()}")

    def textplaincolor(self):
        self.selected_color8 = QColorDialog.getColor()
        if self.selected_color8.isValid():
            self.p.appendHtml(f"<span style='background-color: {self.selected_color8.name()};'>{self.p.toPlainText()}</p>")

App = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(App.exec())















def mousePressEvent(self, event):
    if self.instrument == 'brush':
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()
    else:
        if self.instrument == 'line':
            self.objects.append(Line(event.x(), event.y(), event.x(), event.y()))
            self.update()
        elif self.instrument == 'circle':
            self.objects.append(Circle(event.x(), event.y(), event.x(), event.y()))
            self.update()
        elif self.instrument == 'rect':
            self.objects.append(Rect(event.x(), event.y(), event.x(), event.y()))
            self.update()


def mouseMoveEvent(self, event):
    if self.instrument == 'brush':
        painter = QPainter(self.image)
        if (event.buttons() and Qt.LeftButton) and self.drawing:
            painter.setPen(QPen(self.brushColor, self.brushSize,
                                self.brushline, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()
    if self.instrument == 'line':
        self.objects[-1].ex = event.x()
        self.objects[-1].ey = event.y()
        self.update()
    elif self.instrument == 'circle':
        self.objects[-1].x = event.x()
        self.objects[-1].y = event.y()
        self.update()

    elif self.instrument == 'rect':
        self.objects[-1].x = event.x()
        self.objects[-1].y = event.y()
        self.update()


def mouseReleaseEvent(self, event):
    if event.button() == Qt.LeftButton:
        self.drawing = False


# Холст ###############################################################
def paintEvent(self, event):
    if self.instrument == 'brush':
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())
    else:
        self.painterfigur = QPainter(self.image2)
        self.painterfigur.begin(self)
        for obj in self.objects:
            obj.draw(self.painterfigur)
        self.painterfigur.end()