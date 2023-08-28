from PyQt5.Qt import *
from PIL import Image
import sys
import matplotlib.pyplot as plt
import numpy as np



class Figur3d(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Текстовый файл')
        self.setWindowIcon(QIcon('перо.jpg'))
        self.btn = QPushButton(self)
        self.btn.clicked.connect(self.main)


    def cubes(self, sides):
        data = np.ones(sides)
        fig = plt.figure(figsize=(9, 9))
        ax = fig.add_subplot(111, projection='3d')
        ax.voxels(data, facecolors="yellow")
        plt.show()

# def Sphere(sides):
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
#     ax.set_aspect('equal')
#
#     u = np.linspace(0, 2 * np.pi, 100)
#     v = np.linspace(0, np.pi, 100)
#
#     x = 1 * np.outer(np.cos(u), np.sin(v))
#     y = 1 * np.outer(np.sin(u), np.sin(v))
#     z = 1 * np.outer(np.ones(np.size(u)), np.cos(v))
#
#     elev = 10.0
#     rot = 80.0 / 180 * np.pi
#     ax.plot_surface(x, y, z, rstride=4, cstride=4, color='b', linewidth=0, alpha=0.5)
#     a = np.array([-np.sin(elev / 180 * np.pi), 0, np.cos(elev / 180 * np.pi)])
#     b = np.array([0, 1, 0])
#     b = b * np.cos(rot) + np.cross(a, b) * np.sin(rot) + a * np.dot(a, b) * (1 - np.cos(rot))
#     ax.plot(np.sin(u), np.cos(u), 0, color='k', linestyle='dashed')
#     horiz_front = np.linspace(0, np.pi, 100)
#     ax.plot(np.sin(horiz_front), np.cos(horiz_front), 0, color='k')
#     vert_front = np.linspace(np.pi / 2, 3 * np.pi / 2, 100)
#     ax.plot(a[0] * np.sin(u) + b[0] * np.cos(u), b[1] * np.cos(u), a[2] * np.sin(u) + b[2] * np.cos(u), color='k',
#             linestyle='dashed')
#     ax.plot(a[0] * np.sin(vert_front) + b[0] * np.cos(vert_front), b[1] * np.cos(vert_front),
#             a[2] * np.sin(vert_front) + b[2] * np.cos(vert_front), color='k')
#
#     ax.view_init(elev=elev, azim=0)
#
#     plt.show()

    def main(self):
        sides = np.array([ 2, 2, 2 ])
        self.cubes(sides)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Figur3d()
    ex.show()
    sys.exit(app.exec_())
