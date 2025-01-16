import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QDoubleSpinBox, QLabel, QWidget, QHBoxLayout, QDockWidget
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

vertices = np.array([
    [1, 1, 0], [1, 6, 0], [2, 1, 0], [2, 6, 0], [2, 3, 0], [2, 4, 0],
    [4, 1, 0], [5, 1, 0], [4, 6, 0], [5, 6, 0],
    [1, 1, 1], [1, 6, 1], [2, 1, 1], [2, 6, 1], [2, 3, 1], [2, 4, 1],
    [4, 1, 1], [5, 1, 1], [4, 6, 1], [5, 6, 1]
])

faces = [
    [0, 1, 3, 2], [4, 5, 7, 6], [5, 4, 9, 8], [10, 11, 13, 12],
    [14, 15, 17, 16], [15, 14, 19, 18], [0, 10, 11, 1],
    [1, 3, 11, 13], [13, 3, 5, 15], [5, 15, 18, 8], [8, 18, 19, 9],
    [19, 9, 4, 14], [5, 15, 17, 7], [7, 17, 16, 6], [16, 6, 4, 14],
    [14, 4, 2, 12], [12, 2, 0, 10]
]

class Matplotlib3D(QWidget):
    def __init__(self):
        super().__init__()

        self.vertices = vertices
        self.faces = faces
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvas(self.fig)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.scale_factor = 1.0
        self.translation = np.array([0.0, 0.0, 0.0])
        self.current_projection = None

        self.plot_letter_k()

    def plot_letter_k(self):
        self.ax.clear()
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_xlim(-5, 10)
        self.ax.set_ylim(-5, 10)
        self.ax.set_zlim(-5, 10)

        transformed_vertices = self.vertices * self.scale_factor + self.translation

        poly3d = [[transformed_vertices[vert_id] for vert_id in face] for face in self.faces]
        self.ax.add_collection3d(Poly3DCollection(poly3d, alpha=0.5, edgecolor='k'))

        for vert in transformed_vertices:
            self.ax.scatter(*vert, color="r", s=50)

        self.canvas.draw()

    def apply_shift(self, dx, dy, dz):
        self.translation += np.array([dx, dy, dz])
        self.plot_letter_k()

    def scale(self, factor):
        self.scale_factor *= factor
        self.plot_letter_k()

    def reset(self):
        self.scale_factor = 1.0
        self.translation = np.array([0.0, 0.0, 0.0])
        self.plot_letter_k()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("3D Viewer: Буква К")

        self.viewer = Matplotlib3D()
        self.setCentralWidget(self.viewer)

        controls = QWidget()
        controls_layout = QVBoxLayout()
        controls.setLayout(controls_layout)

        shift_controls = QHBoxLayout()
        self.shift_x = QDoubleSpinBox()
        self.shift_y = QDoubleSpinBox()
        self.shift_z = QDoubleSpinBox()
        shift_button = QPushButton("Сдвинуть")
        shift_button.clicked.connect(lambda: self.viewer.apply_shift(self.shift_x.value(), self.shift_y.value(), self.shift_z.value()))

        shift_controls.addWidget(QLabel("Сдвиг X:"))
        shift_controls.addWidget(self.shift_x)
        shift_controls.addWidget(QLabel("Сдвиг Y:"))
        shift_controls.addWidget(self.shift_y)
        shift_controls.addWidget(QLabel("Сдвиг Z:"))
        shift_controls.addWidget(self.shift_z)
        shift_controls.addWidget(shift_button)

        controls_layout.addLayout(shift_controls)

        scale_controls = QHBoxLayout()
        scale_up_button = QPushButton("Масштаб +")
        scale_down_button = QPushButton("Масштаб -")
        reset_button = QPushButton("Сбросить")

        scale_up_button.clicked.connect(lambda: self.viewer.scale(1.1))
        scale_down_button.clicked.connect(lambda: self.viewer.scale(0.9))
        reset_button.clicked.connect(self.viewer.reset)

        scale_controls.addWidget(scale_up_button)
        scale_controls.addWidget(scale_down_button)
        scale_controls.addWidget(reset_button)

        controls_layout.addLayout(scale_controls)

        dock = QDockWidget("Панель управления", self)
        dock.setWidget(controls)
        self.addDockWidget(0x2, dock)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
