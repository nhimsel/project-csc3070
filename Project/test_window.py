from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PySide6.QtCore import Signal
import sys

class MainWindow(QWidget):
    switchGif = Signal(str)

    def __init__(self, buddy_window):
        super().__init__()

        self.buddy_window = buddy_window

        # Create buttons
        self.button1 = QPushButton("default")
        self.button2 = QPushButton("smile")
        self.button3 = QPushButton("talk")
        self.button4 = QPushButton("wave")
        self.button5 = QPushButton("blink")
        self.button6 = QPushButton("CrazyThrowCrop")
        self.button7 = QPushButton("return")

        # Connect signals
        self.button1.clicked.connect(self.on_button1_clicked)
        self.button2.clicked.connect(self.on_button2_clicked)
        self.button3.clicked.connect(self.on_button3_clicked)
        self.button4.clicked.connect(self.on_button4_clicked)
        self.button5.clicked.connect(self.on_button5_clicked)
        self.button6.clicked.connect(self.on_button6_clicked)
        self.button7.clicked.connect(self.on_button7_clicked)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.button4)
        layout.addWidget(self.button5)
        layout.addWidget(self.button6)
        layout.addWidget(self.button7)

        self.setLayout(layout)

    def on_button1_clicked(self):
        self.switchGif.emit("default.gif")
    def on_button2_clicked(self):
        self.switchGif.emit("smile.gif")
    def on_button3_clicked(self):
        self.switchGif.emit("talk.gif")
    def on_button4_clicked(self):
        self.switchGif.emit("wave.gif")
    def on_button5_clicked(self):
        self.switchGif.emit("blink.gif")
    def on_button6_clicked(self):
        self.switchGif.emit("CrazyThrowCrop.gif")
    def on_button7_clicked(self):
        self.buddy_window.move_to_bottom_right()
