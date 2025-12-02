from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import QEvent, Qt, QRunnable, Slot, Signal, QThreadPool, QObject

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Window
from openai import send_message


class ChatWindow(QMainWindow):
    chat_response = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Window()
        self.ui.setupUi(self)

        self.setWindowTitle("test")
        self.ui.textEdit.installEventFilter(self)
        self.ui.pushButton.clicked.connect(self.message_send)

    def message_send(self):
        self.ui.pushButton.setDisabled(True)
        input=self.ui.textEdit.toPlainText()
        #send_message(input, self.ui.textEdit_2)
        #self.ui.textEdit_2.setText(send_message(input))
        worker = message_worker(input)
        worker.signals.result.connect(self.restore_ui)
        QThreadPool.globalInstance().start(worker)

    def restore_ui(self, response):
        self.chat_response.emit(response)
        self.ui.textEdit_2.setText(response)
        self.ui.textEdit.clear()
        self.ui.pushButton.setEnabled(True)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress and obj is self.ui.textEdit:
            if event.key() == Qt.Key.Key_Return and self.ui.textEdit.hasFocus():
                self.message_send()
        return super().eventFilter(obj,event)
    
    def move_then_show(self, x:int, y:int):
        #x and y are coords of buddy_window
        self.move(x-self.width(),y-self.height())
        self.show()

    def move_no_show(self, x:int, y:int):
        #x and y are coords of buddy_window
        self.move(x-self.width(),y-self.height())

    def closeEvent(self, event):
        event.ignore()
        self.hide()

class message_worker(QRunnable):
    def __init__(self, input):
        super().__init__()
        self.input= input
        self.signals = message_worker_signal()

    @Slot()
    def run(self):
        try:
            response = send_message(self.input)
            self.signals.result.emit(response)
        except Exception as e:
            self.signals.result.emit("error")

class message_worker_signal(QObject):
    result = Signal(str)
