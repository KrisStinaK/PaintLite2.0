from PyQt5.Qt import *
from PIL import Image, ImageFilter
import sys
from ProjectY import Ui_MainWindow2


class UndoCommand(QUndoCommand):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.mPrevImage = parent.image.copy()
        self.mCurrImage = parent.image.copy()

    def undo(self):
        self.mCurrImage = self.parent.image.copy()
        self.parent.image = self.mPrevImage
        self.parent.update()

    def redo(self):
        self.parent.image = self.mCurrImage
        self.parent.update()


class MyWidget(QMainWindow, Ui_MainWindow2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.objects = []
        self.instrument = 'brush'
        self.start_pos = QPointF()
        self.end_pos = QPointF()

        self.label2 = QLabel(self)
        self.label2.hide()
        self.setWindowTitle("Крутой Paint")
        self.setWindowIcon(QIcon('periptic5.jpg'))
        self.setGeometry(100, 100, 1350, 1000)

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

        self.is_pressed = False

        self.mUndoStack = QUndoStack(self)
        self.mUndoStack.setUndoLimit(20)

        self.mUndoStack.canUndoChanged.connect(self.can_undo_changed)
        self.mUndoStack.canRedoChanged.connect(self.can_redo_changed)

        self.action_33.triggered.connect(self.mUndoStack.undo)
        self.action_39.triggered.connect(self.mUndoStack.redo)

        self.can_undo_changed(self.mUndoStack.canUndo())
        self.can_redo_changed(self.mUndoStack.canRedo())

        self.p = QPlainTextEdit(self)
        self.p.resize(700, 950)
        self.p.move(300, 44)
        self.p.hide()

        self.action_4.triggered.connect(self.toolb)
        self.toolBar.hide()
        self.action_7.triggered.connect(self.tool2)
        self.toolBar_3.hide()
        self.action_8.triggered.connect(self.tool3)
        self.toolBar_2.hide()

        self.action.triggered.connect(self.savef)
        self.action_2.triggered.connect(self.clearf)
        self.action_3.triggered.connect(self.close)

        self.action_5.triggered.connect(self.Background)
        self.action_6.triggered.connect(self.Draw)

        self.action_9.triggered.connect(self.Text)
        self.action_10.triggered.connect(self.Text_save)
        self.action_10.setEnabled(False)
        self.action_11.triggered.connect(self.getFont)
        self.action_11.setEnabled(False)
        self.action_12.triggered.connect(self.fontColor)
        self.action_12.setEnabled(False)
        self.action_13.triggered.connect(self.onTextChanged)
        self.action_13.setEnabled(False)
        self.action_14.triggered.connect(self.textplaincolor)
        self.action_14.setEnabled(False)

        self.action_15.triggered.connect(self.Foto)
        self.action_16.triggered.connect(self.rotate_right)
        self.action_16.setEnabled(False)
        self.action_17.triggered.connect(self.rotate2_left)
        self.action_17.setEnabled(False)
        self.action_45.triggered.connect(self.rotate_45_left)
        self.action_45.setEnabled(False)
        self.action_46.triggered.connect(self.rotate_45_right)
        self.action_46.setEnabled(False)
        self.action_180.triggered.connect(self.rotate_180_right)
        self.action_180.setEnabled(False)
        self.action_16.triggered.connect(self.rotate_right)
        self.action_16.setEnabled(False)
        self.action_18.triggered.connect(self.Delfoto)
        self.action_18.setEnabled(False)
        self.action_20.triggered.connect(self.saveimg)
        self.action_20.setEnabled(False)

        self.action_21.triggered.connect(self.Negative)
        self.action_21.setEnabled(False)
        self.action_22.triggered.connect(self.invert)
        self.action_22.setEnabled(False)
        self.action_23.triggered.connect(self.curve)
        self.action_23.setEnabled(False)
        self.action_24.triggered.connect(self.OriginalFoto)
        self.action_24.setEnabled(False)

        self.action_26.triggered.connect(self.setRect)
        self.action_27.triggered.connect(self.setLine)
        self.action_28.triggered.connect(self.setCircle)

        self.action_29.triggered.connect(self.setBrush)
        self.action_30.triggered.connect(self.Fill)
        self.action_31.triggered.connect(self.Eraser)

        self.action_35.triggered.connect(self.SolidLine)
        self.action_1.triggered.connect(self.DashLine)
        self.action_36.triggered.connect(self.DashDotLine)
        self.action_37.triggered.connect(self.DotLine)
        self.action_38.triggered.connect(self.DashDotDotLine)

        self.action2.triggered.connect(self.Pixel_2)
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

        self.action_34.triggered.connect(self.Color)

        self.action_19.triggered.connect(self.setRect2)
        self.action_32.triggered.connect(self.setCircle2)

        self.action_42.triggered.connect(self.slider)
        self.action_42.setEnabled(False)
        self.verticalSlider.hide()
        self.verticalSlider.setMinimum(0)
        self.verticalSlider.setMaximum(255)
        self.verticalSlider.setValue(255)
        self.verticalSlider.valueChanged[int].connect(self.visibility)

        self.save = 'save.png'

    def slider(self):
        self.verticalSlider.show()

    def can_undo_changed(self, enabled):
        self.action_33.setEnabled(enabled)

    def can_redo_changed(self, enabled):
        self.action_39.setEnabled(enabled)

    def make_undo_command(self):
        self.mUndoStack.push(UndoCommand(self))

    def toolb(self):
        self.toolBar.show()
        self.toolBar_3.hide()
        self.toolBar_2.hide()
        self.p.hide()
        self.label2.hide()

    def tool2(self):
        self.toolBar.hide()
        self.toolBar_3.show()
        self.toolBar_2.hide()
        self.label2.hide()

    def tool3(self):
        self.toolBar.hide()
        self.toolBar_3.hide()
        self.toolBar_2.show()
        self.p.hide()
        self.label2.show()

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

    # мышь ##############################################################
    def draw(self, canvas):
        painter = QPainter(canvas)

        if self.instrument == 'brush':
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine))
            painter.drawImage(self.rect(), self.image, self.image.rect())

        elif self.instrument == 'line':
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine))
            painter.drawLine(self.start_pos, self.end_pos)

        elif self.instrument == 'circle':
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine))
            painter.drawEllipse(QRectF(self.start_pos, self.end_pos))

        elif self.instrument == 'rect':
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine))
            painter.drawRect(QRectF(self.start_pos, self.end_pos))

        elif self.instrument == 'circle2':
            painter.setBrush(QBrush(self.brushColor))
            painter.drawEllipse(QRectF(self.start_pos, self.end_pos))

        elif self.instrument == 'rect2':
            painter.setBrush(QBrush(self.brushColor))
            painter.drawRect(QRectF(self.start_pos, self.end_pos))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.image.rect(), self.image)

        # Рисуем на виджете
        self.draw(self)

    def mousePressEvent(self, event):
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
        self.make_undo_command()

        self.draw(self.image)
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Z and event.modifiers() == Qt.ControlModifier:
            self.mUndoStack.undo()
        elif event.key() == Qt.Key_Y and event.modifiers() == Qt.ControlModifier:
            self.mUndoStack.redo()

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
        self.p.hide()
        self.label2.hide()
        self.image = QImage(self.size(), QImage.Format_ARGB32)
        self.image.fill(Qt.white)

    def Background(self):
        self.backgroundfile = QFileDialog.getOpenFileName(self, 'Выберите картинку', '')[0]
        if self.backgroundfile == '':
            return
        self.image.load(self.backgroundfile)

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

    def DashDotLine(self):
        self.brushline = Qt.DashDotLine

    def DotLine(self):
        self.brushline = Qt.DotLine

    def DashDotDotLine(self):
        self.brushline = Qt.DashDotDotLine

    def SolidLine(self):
        self.brushline = Qt.SolidLine

    # text ###################################################################
    def Text(self):
        self.p.show()
        self.action_10.setEnabled(True)
        self.action_11.setEnabled(True)
        self.action_12.setEnabled(True)
        self.action_13.setEnabled(True)
        self.action_14.setEnabled(True)
        # self.Delfoto()

    def Text_save(self):
        file, _ = QFileDialog.getSaveFileName(self, "Save File", "",
                                              "(*.txt);;")

        if file == "":
            return
        f = open(file, mode='w', encoding='utf8')
        f.write(self.p.toPlainText())
        f.close()

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

    def onTextChanged(self):
        self.selected_color7 = QColorDialog.getColor()
        if self.selected_color7.isValid():
            self.p.setStyleSheet(
                f"background-color: {self.selected_color7.name()}")

    def textplaincolor(self):
        self.selected_color8 = QColorDialog.getColor()
        if self.selected_color8.isValid():
            self.p.appendHtml(
                f"<span style='background-color: {self.selected_color8.name()};'>{self.p.toPlainText()}</p>")

    # Foto ########################################################################
    def Foto(self):
        self.p.hide()
        self.label2.show()
        self.filename = QFileDialog.getOpenFileName(self, 'Выберите картинку', '')[0]
        if self.filename == '':
            return
        self.img = QPixmap(self.filename)
        self.foto_orig = self.img
        self.label2.setPixmap(self.img)
        self.label2.resize(1300, 950)
        self.label2.move(275, 21)

        self.action_16.setEnabled(True)
        self.action_17.setEnabled(True)
        self.action_45.setEnabled(True)
        self.action_46.setEnabled(True)
        self.action_180.setEnabled(True)
        self.action_16.setEnabled(True)
        self.action_18.setEnabled(True)
        self.action_20.setEnabled(True)
        self.action_21.setEnabled(True)
        self.action_22.setEnabled(True)
        self.action_23.setEnabled(True)
        self.action_24.setEnabled(True)
        self.action_42.setEnabled(True)

        self.original = Image.open(self.filename)
        self.current = Image.open(self.filename)

        self.rotation = 0

    def visibility(self, value):
        im = Image.open(self.filename)
        im = im.convert('RGBA')
        im.putalpha(value)
        im.save(self.save)
        self.img = QPixmap(self.save)
        self.to_show = self.img.copy()
        self.label2.setPixmap(self.to_show)

        self.original = Image.open(self.filename)
        self.current = Image.open(self.filename)

    def Delfoto(self):
        self.label2.hide()
        self.action_16.setEnabled(False)
        self.action_17.setEnabled(False)
        self.action_45.setEnabled(False)
        self.action_46.setEnabled(False)
        self.action_180.setEnabled(False)
        self.action_16.setEnabled(False)
        self.action_18.setEnabled(False)
        self.action_20.setEnabled(False)
        self.action_21.setEnabled(False)
        self.action_22.setEnabled(False)
        self.action_23.setEnabled(False)
        self.action_24.setEnabled(False)
        self.action_42.setEnabled(False)

    def OriginalFoto(self):
        self.action_42.setEnabled(True)
        self.label2.setPixmap(self.foto_orig)
        self.update()

        self.original = Image.open(self.filename)
        self.current = Image.open(self.filename)

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

    def saveimg(self):
        foto, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                              "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if foto == '':
            return
        self.img.save(foto)

    def Negative(self):
        self.action_42.setEnabled(False)
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
        self.action_42.setEnabled(False)
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
        self.action_42.setEnabled(False)
        x, y = self.current.size
        pixels = self.current.load()
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                pixels[i, j] = r, b, g
        self.current.save('current.png')
        self.label2.setPixmap(QPixmap('current.png'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
