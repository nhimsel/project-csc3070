from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
import sys
from buddy_window import ShapedWindow

class MainWindow(QWidget):
    def __init__(self, buddy:ShapedWindow):
        super().__init__()
        # Create buttons
        self.button1 = QPushButton("feesh")
        self.button2 = QPushButton("feesh-2")

        # Connect signals
        self.button1.clicked.connect(self.on_button1_clicked)
        self.button2.clicked.connect(self.on_button2_clicked)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)

        self.buddy = buddy

        self.setLayout(layout)

    def on_button1_clicked(self):
        self.buddy.switch_gif("feesh")

    def on_button2_clicked(self):
        self.buddy.switch_gif("feesh-2")
