from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PySide6.QtCore import Signal
import sys

class MainWindow(QWidget):
    switchGif = Signal(str)

    def __init__(self, buddy_window):
        super().__init__()

        self.buddy_window = buddy_window

        # Create buttons
        self.button1 = QPushButton("feesh")
        self.button2 = QPushButton("feesh-2")
        self.button3 = QPushButton("cat")
        self.button4 = QPushButton("Return")

        # Connect signals
        self.button1.clicked.connect(self.on_button1_clicked)
        self.button2.clicked.connect(self.on_button2_clicked)
        self.button3.clicked.connect(self.on_button3_clicked)
        self.button4.clicked.connect(self.on_button4_clicked)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.button4)

        self.setLayout(layout)

    def on_button1_clicked(self):
        self.switchGif.emit("feesh")

    def on_button2_clicked(self):
        self.switchGif.emit("feesh-2")
    def on_button3_clicked(self):
        self.switchGif.emit("cat")
    def on_button4_clicked(self):
        self.buddy_window.move_to_bottom_right()
