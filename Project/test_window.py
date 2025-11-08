from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PySide6.QtCore import Signal
import sys

class MainWindow(QWidget):
    switchGif = Signal(str)

    def __init__(self):
        super().__init__()
        # Create buttons
        self.button1 = QPushButton("feesh")
        self.button2 = QPushButton("feesh-2")
        self.button3 = QPushButton("cat")

        # Connect signals
        self.button1.clicked.connect(self.on_button1_clicked)
        self.button2.clicked.connect(self.on_button2_clicked)
        self.button3.clicked.connect(self.on_button3_clicked)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)

        self.setLayout(layout)

    def on_button1_clicked(self):
        self.switchGif.emit("feesh")

    def on_button2_clicked(self):
        self.switchGif.emit("feesh-2")
    def on_button3_clicked(self):
        self.switchGif.emit("cat")
