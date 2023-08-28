from PyQt5.Qt import *
from PIL import Image
import sys
from UIproject import Ui_MainWindow
from UIproject_2 import Ui_MainWindow_2
from UIproject_3 import Ui_MainWindow_3
from UIproject_4 import Ui_MainWindow_4


class MyWidget(QMainWindow, Ui_MainWindow, QPushButton):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('перо.jpg'))
        self.setStyleSheet("background-color: rgb(80, 80, 80);")
        self.pushButton.setStyleSheet("background-color: white")
        self.pushButton_2.setStyleSheet("background-color: white")
        self.pushButton_3.setStyleSheet("background-color: white")
        self.label.setStyleSheet("color: white")
        self.init_handlers()
        self.init_handlers2()
        self.init_handlers3()
        self.btn = QPushButton(self)
        self.btn2 = QPushButton(self)
        self.init_ui()

    def init_ui(self):
        self.btn.resize(50, 50)
        self.btn.move(0, 0)
        self.btn.setStyleSheet('QPushButton{border: none; background: pink;}')

        self.btn2.resize(50, 50)
        self.btn2.move(0, 0)
        self.btn2.setStyleSheet('QPushButton{border: none; background: white;}')

        animation = QPropertyAnimation(self.btn, b'pos', self)

        animation.setKeyValueAt(0, QPoint(0, 0))
        animation.setKeyValueAt(0.25, QPoint(1129, 0))
        animation.setKeyValueAt(0.5, QPoint(1129, 1129))
        animation.setKeyValueAt(0.75, QPoint(0, 1129))
        animation.setKeyValueAt(1, QPoint(0, 0))
        animation.setDuration(25000)
        animation.start()

        animation2 = QPropertyAnimation(self.btn2, b'pos', self)

        animation2.setKeyValueAt(0, QPoint(0, 0))
        animation2.setKeyValueAt(0.25, QPoint(0, 1129))
        animation2.setKeyValueAt(0.5, QPoint(0, 0))
        animation2.setKeyValueAt(0.75, QPoint(1129, 0))
        animation2.setKeyValueAt(1, QPoint(1129, 1129))
        animation2.setDuration(25000)
        animation2.start()

    def init_handlers(self):
        self.pushButton.clicked.connect(self.show_window_2)

    def init_handlers2(self):
        self.pushButton_3.clicked.connect(self.show_window_3)

    def init_handlers3(self):
        self.pushButton_2.clicked.connect(self.show_window_4)

    def show_window_2(self):
        self.w2 = MyWidget2()
        self.w2.show()
        self.hide()

    def show_window_3(self):
        self.w3 = MyWidget3()
        self.w3.show()
        self.hide()

    def show_window_4(self):
        self.w4 = MyWidget4()
        self.w4.show()
        self.hide()


class MyWidget2(QMainWindow, Ui_MainWindow_2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('перо.jpg'))
        self.setWindowTitle('paint на минималках')

        self.objects = []
        self.instrument = 'brush'
        self.start_pos = QPointF()
        self.end_pos = QPointF()

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.lastPoint = QPoint()
        self.drawing = False
        self.brushSize = 2
        self.brushSize2 = 2
        self.brushline = Qt.SolidLine
        self.brushColor = Qt.black
        self.brushColor2 = Qt.black
        self.textsize = 2
        self.lastic = Qt.white

        self.action.triggered.connect(self.Menu)
        self.action_2.triggered.connect(self.savef)
        self.action_3.triggered.connect(self.clearf)
        self.action_9.triggered.connect(self.closeEvent)
        self.action_6.triggered.connect(self.Fill)
        self.action_7.triggered.connect(self.Eraser)

        self.action_5.triggered.connect(self.SolidLine)
        self.action_1.triggered.connect(self.DashLine)
        self.action_8.triggered.connect(self.DashDotLine)
        self.action_17.triggered.connect(self.DotLine)
        self.action_18.triggered.connect(self.DashDotDotLine)

        self.action2px.triggered.connect(self.Pixel_2)
        self.action4px.triggered.connect(self.Pixel_4)
        self.action7px.triggered.connect(self.Pixel_7)
        self.action9px.triggered.connect(self.Pixel_9)
        self.action12px.triggered.connect(self.Pixel_12)
        self.action15px.triggered.connect(self.Pixel_15)
        self.action17px.triggered.connect(self.Pixel_17)
        self.action20px.triggered.connect(self.Pixel_20)
        self.action25px.triggered.connect(self.Pixel_25)
        self.action30px.triggered.connect(self.Pixel_30)
        self.action35px.triggered.connect(self.Pixel_35)
        self.action40px.triggered.connect(self.Pixel_40)
        self.action45px.triggered.connect(self.Pixel_45)
        self.action50px.triggered.connect(self.Pixel_50)

        self.action_10.triggered.connect(self.setLine)
        self.action_11.triggered.connect(self.setCircle)
        self.action_12.triggered.connect(self.setRect)
        self.action_13.triggered.connect(self.setCircle2)
        self.action_14.triggered.connect(self.setRect2)
        self.action_16.triggered.connect(self.Color)

    def Background(self):
        self.backgroundfile = QFileDialog.getOpenFileName(self, 'Выберите картинку', '')[0]
        if self.backgroundfile == '':
            return
        self.image.load(self.backgroundfile)

    def closeEvent(self, event):
        msg = QMessageBox(self)
        msg.setWindowTitle("Выход")
        msg.setIcon(QMessageBox.Question)
        msg.setText("Вы хотите сохранить файл?")

        buttonSave = msg.addButton("Сохранить", QMessageBox.YesRole)
        buttonAceptar  = msg.addButton("Не сохранять", QMessageBox.YesRole)
        buttonCancelar = msg.addButton("Отменить", QMessageBox.RejectRole)
        msg.setDefaultButton(buttonAceptar)
        msg.exec_()

        if msg.clickedButton() == buttonAceptar:
            self.close()
        elif msg.clickedButton() == buttonSave:
            self.savef()
        elif msg.clickedButton() == buttonCancelar:
            return

    # инструменты
    def setBrush(self):
        self.instrument = 'brush'
        self.Color()

    def setLine(self):
        self.instrument = 'line'

    def setCircle(self):
        self.instrument = 'circle'

    def setRect(self):
        self.instrument = 'rect'

    def setRect2(self):
        self.instrument = 'rect2'

    def setCircle2(self):
        self.instrument = 'circle2'

    def draw(self, canvas):
        painter = QPainter(canvas)

        if self.instrument == 'brush':
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine))
            painter.drawImage(self.rect(), self.image, self.image.rect())
            self.update()

        elif self.instrument == 'line':
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine))
            painter.drawLine(self.start_pos, self.end_pos)
            self.update()

        elif self.instrument == 'circle':
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine))
            painter.drawEllipse(QRectF(self.start_pos, self.end_pos))
            self.update()

        elif self.instrument == 'rect':
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine))
            painter.drawRect(QRectF(self.start_pos, self.end_pos))
            self.update()

        elif self.instrument == 'circle2':
            painter.setBrush(QBrush(self.brushColor))
            painter.drawEllipse(QRectF(self.start_pos, self.end_pos))
            self.update()

        elif self.instrument == 'rect2':
            painter.setBrush(QBrush(self.brushColor))
            painter.drawRect(QRectF(self.start_pos, self.end_pos))
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.image.rect(), self.image)

        # Рисуем на виджете
        self.draw(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.Color()
        if self.instrument == 'brush':
            if event.button() == Qt.LeftButton:
                self.drawing = True
                self.lastPoint = event.pos()
        else:
            self.start_pos = event.pos()
            self.objects.clear()

    def mouseMoveEvent(self, event):
        if self.instrument == 'brush':
            painter = QPainter(self.image)
            if (event.buttons() and Qt.LeftButton) and self.drawing:
                painter.setPen(QPen(self.brushColor, self.brushSize,
                                    self.brushline, Qt.RoundCap, Qt.RoundJoin))
                painter.drawLine(self.lastPoint, event.pos())
                self.lastPoint = event.pos()
                self.update()

        elif event.buttons() and Qt.LeftButton:
            self.end_pos = event.pos()
            self.objects.append(self.end_pos)
            self.update()

    def mouseReleaseEvent(self, event):
        self.end_pos = event.pos()
        self.objects.append(self.end_pos)

        self.draw(self.image)
        self.update()

    def Menu(self, event):
        self.closeEvent(event)
        ex.show()
        self.hide()

    def savef(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if filePath == "":
            return
        self.image.save(filePath)

    def clearf(self):
        self.image.fill(Qt.white)
        self.update()

    def Draw(self):
        self.instrument = 'brush'

    def Color(self):
        self.selected_color = QColorDialog.getColor()
        if self.selected_color.isValid():
            self.brushColor = QColor(*self.selected_color.getRgb())

    def Eraser(self):
        self.brushColor = Qt.white
        self.brushline = Qt.SolidLine
        self.instrument = 'brush'
        self.brushSize = self.brushSize2

    def Fill(self):
        self.selected_color_fill = QColorDialog.getColor()
        if self.selected_color_fill.isValid():
            self.brushColor_fill = QColor(*self.selected_color_fill.getRgb())
            self.image.fill(QColor(self.brushColor_fill))
            self.update()

    # size brush

    def Pixel_2(self):
        self.brushSize = 2

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

    def Pixel_35(self):
        self.brushSize = 35

    def Pixel_40(self):
        self.brushSize = 40

    def Pixel_45(self):
        self.brushSize = 45

    def Pixel_50(self):
        self.brushSize = 50

    # line
    def DashLine(self):
        self.brushline = Qt.DashLine
        self.instrument = 'brush'

    def DashDotLine(self):
        self.brushline = Qt.DashDotLine
        self.instrument = 'brush'

    def DotLine(self):
        self.brushline = Qt.DotLine
        self.instrument = 'brush'

    def DashDotDotLine(self):
        self.brushline = Qt.DashDotDotLine
        self.instrument = 'brush'

    def SolidLine(self):
        self.brushline = Qt.SolidLine
        self.instrument = 'brush'


class MyWidget3(QMainWindow, Ui_MainWindow_3):
    def __init__(self, parent=None):
        super(MyWidget3, self).__init__(parent)
        self.setupUi(self)

        self.label2 = QLabel(self)
        self.setCentralWidget(self.label2)
        self.label2.hide()
        self.setWindowTitle("Обработка изображения")
        self.setWindowIcon(QIcon('перо.jpg'))
        self.action.triggered.connect(self.Menu)
        self.action_2.triggered.connect(self.Foto)
        self.action_3.triggered.connect(self.saveimg)
        self.action_3.triggered.connect(self.saveimg)
        self.action_3.setEnabled(False)
        self.action_4.triggered.connect(self.OriginalFoto)
        self.action_4.setEnabled(False)
        self.action_11.triggered.connect(self.close)

        self.action_5.triggered.connect(self.rotate_right)
        self.action_5.setEnabled(False)
        self.action_6.triggered.connect(self.rotate2_left)
        self.action_6.setEnabled(False)
        self.action_46.triggered.connect(self.rotate_45_right)
        self.action_46.setEnabled(False)
        self.action_45.triggered.connect(self.rotate_45_left)
        self.action_45.setEnabled(False)
        self.action_180.triggered.connect(self.rotate_180)
        self.action_180.setEnabled(False)

        self.action_8.triggered.connect(self.Negative)
        self.action_8.setEnabled(False)
        self.action_9.triggered.connect(self.invert)
        self.action_9.setEnabled(False)
        self.action_10.triggered.connect(self.curve)
        self.action_10.setEnabled(False)
        self.action_12.triggered.connect(self.Overlay)
        self.action_12.setEnabled(False)
        self.action_13.triggered.connect(self.curve)
        self.action_13.setEnabled(False)
        self.action_14.triggered.connect(self.Fotored)
        self.action_14.setEnabled(False)

    def paint(self):
        painter = QPainter(self.img)
        painter.begin(self)
        img = QPixmap("Зима.jpg")
        painter.drawPixmap(0, 0, img)
        painter.drawPixmap(0, 0, QPixmap("Мишки.jpg"))
        painter.end()

    def closeEvent(self, event):
        msg = QMessageBox(self)
        msg.setWindowTitle("Выход")
        msg.setIcon(QMessageBox.Question)
        msg.setText("Вы хотите сохранить фото?")

        buttonSave = msg.addButton("Сохранить", QMessageBox.YesRole)
        buttonAceptar  = msg.addButton("Не сохранять", QMessageBox.YesRole)
        buttonCancelar = msg.addButton("Отменить", QMessageBox.RejectRole)
        msg.setDefaultButton(buttonAceptar)
        msg.exec_()

        if msg.clickedButton() == buttonAceptar:
            self.close()
        elif msg.clickedButton() == buttonSave:
            self.saveimg()
        elif msg.clickedButton() == buttonCancelar:
            return

    def Menu(self, p):
        self.closeEvent(p)
        ex.show()
        self.hide()

# Foto ########################################################################
    def Foto(self):
        self.label2.show()

        self.filename = QFileDialog.getOpenFileName(self, 'Выберите картинку', '')[0]
        if self.filename == '':
            return

        self.img = QPixmap(self.filename)
        self.foto_orig = self.img
        self.label2.setPixmap(self.img)
        self.label2.resize(self.img.size())
        self.adjustSize()

        self.action_3.setEnabled(True)
        self.action_4.setEnabled(True)
        self.action_5.setEnabled(True)
        self.action_6.setEnabled(True)
        self.action_45.setEnabled(True)
        self.action_46.setEnabled(True)
        self.action_180.setEnabled(True)
        self.action_8.setEnabled(True)
        self.action_9.setEnabled(True)
        self.action_10.setEnabled(True)
        self.action_12.setEnabled(True)
        self.action_13.setEnabled(True)
        self.action_14.setEnabled(True)

        self.hbox = QHBoxLayout(self)

        self.label2.setPixmap(self.img)

        self.hbox.addWidget(self.label2)
        self.setLayout(self.hbox)

        self.original = Image.open(self.filename)
        self.current = Image.open(self.filename)

        self.rotation = 0

    def Delfoto(self):
        self.label2.hide()

    def OriginalFoto(self):
        self.label2.setPixmap(self.foto_orig)
        self.update()

    def rotate2_left(self):
        self.current = self.current.rotate(90)
        self.current.save('current.png')
        self.label2.setPixmap(QPixmap('current.png'))
        self.rotation = 0

    def rotate_right(self):
        self.current = self.current.rotate(-90)
        self.current.save('current.png')
        self.label2.setPixmap(QPixmap('current.png'))
        self.rotation = 0

    def rotate_45_right(self):
        self.current = self.current.rotate(45)
        self.current.save('current.png')
        self.label2.setPixmap(QPixmap('current.png'))
        self.rotation = 0

    def rotate_45_left(self):
        self.current = self.current.rotate(-45)
        self.current.save('current.png')
        self.label2.setPixmap(QPixmap('current.png'))
        self.rotation = 0

    def rotate_180(self):
        self.current = self.current.rotate(-180)
        self.current.save('current.png')
        self.label2.setPixmap(QPixmap('current.png'))
        self.rotation = 0

    def saveimg(self):
        foto, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if foto == '':
            return
        self.current.save(foto)

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

    def Fotored(self):
        painter = QPainter(self)
        painter.drawPixmap(520, 0, 500, 500, QBitmap(self.filename))

    def Overlay(self):
        filename_2 = QFileDialog.getOpenFileName(self, 'Выберите картинку', '')[0]

        if filename_2 == '':
            return

        painter = QPainter(self.img)
        painter.begin(self)
        img = QPixmap(filename_2)
        painter.drawPixmap(0, 0, img)
        painter.drawPixmap(0, 0, QPixmap(filename_2))
        painter.end()


class MyWidget4(QMainWindow, Ui_MainWindow_4):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Текстовый файл')
        self.setWindowIcon(QIcon('перо.jpg'))
        self.plainTextEdit.hide()
        self.action.triggered.connect(self.Text)
        self.action_2.triggered.connect(self.Text_save)
        self.action_2.setEnabled(False)
        self.action_3.triggered.connect(self.Menu)
        self.action_4.triggered.connect(self.getFont)
        self.action_4.setEnabled(False)
        self.action_5.triggered.connect(self.fontColor)
        self.action_5.setEnabled(False)
        self.action_6.triggered.connect(self.onTextChanged)
        self.action_6.setEnabled(False)
        self.action_8.triggered.connect(self.close)


    def closeEvent(self, event):
        msg = QMessageBox(self)
        msg.setWindowTitle("Выход")
        msg.setIcon(QMessageBox.Question)
        msg.setText("Вы хотите сохранить файл?")

        buttonSave = msg.addButton("Сохранить", QMessageBox.YesRole)
        buttonAceptar = msg.addButton("Не сохранять", QMessageBox.YesRole)
        buttonCancelar = msg.addButton("Отменить", QMessageBox.RejectRole)
        msg.setDefaultButton(buttonAceptar)
        msg.exec_()

        if msg.clickedButton() == buttonAceptar:
            self.close()
        elif msg.clickedButton() == buttonSave:
            self.Text_save()
        elif msg.clickedButton() == buttonCancelar:
            return

    def Menu(self, event):
        self.closeEvent(event)
        ex.show()
        self.hide()

# text ###################################################################
    def Text(self):
        self.plainTextEdit.show()
        self.action_4.setEnabled(True)
        self.action_5.setEnabled(True)
        self.action_6.setEnabled(True)
        self.action_2.setEnabled(True)

    def Text_save(self):
        file, _ = QFileDialog.getSaveFileName(self, "Save File", "",
                                                  "(*.txt);;")

        if file == "":
            return
        f = open(file, mode='w', encoding='utf8')
        f.write(self.plainTextEdit.toPlainText())
        f.close()

    def getFont(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.plainTextEdit.setFont(font)

    def fontColor(self):
        self.selected_color2 = QColorDialog.getColor()
        if self.selected_color2.isValid():
            Palette = QPalette()
            Palette.setColor(QPalette.Text, self.selected_color2)
            self.plainTextEdit.setPalette(Palette)

    def onTextChanged(self):
        self.selected_color3 = QColorDialog.getColor()
        if self.selected_color3.isValid():
            self.plainTextEdit.setStyleSheet(
                f"background-color: {self.selected_color3.name()}")

    def textplaincolor(self):
        self.selected_color8 = QColorDialog.getColor()
        if self.selected_color8.isValid():
            self.plainTextEdit.appendHtml(f"<span style='background-color: {self.selected_color8.name()};'>{self.plainTextEdit.toPlainText()}</p>")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())