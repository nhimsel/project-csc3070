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

        self.setWindowTitle("chat")
        self.ui.textEdit_input.installEventFilter(self)
        self.ui.pushButton.clicked.connect(self.message_send)
        self.conversation_history = []  # Store conversation history

    def message_send(self):
        self.ui.pushButton.setDisabled(True)
        user_input = self.ui.textEdit_input.toPlainText()
        
        # Add user message to history and display
        self.conversation_history.append(("user", user_input))
        self.display_conversation()
        self.ui.textEdit_input.clear()
        
        # Send message asynchronously
        worker = message_worker(user_input)
        worker.signals.result.connect(self.restore_ui)
        QThreadPool.globalInstance().start(worker)

    def restore_ui(self, response):
        self.chat_response.emit(response)
        
        # Add bot message to history and display
        self.conversation_history.append(("bot", response))
        self.display_conversation()
        
        self.ui.pushButton.setEnabled(True)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress and obj is self.ui.textEdit_input:
            if event.key() == Qt.Key.Key_Return and self.ui.textEdit_input.hasFocus():
                self.message_send()
        return super().eventFilter(obj,event)
    
    def display_conversation(self):
        """Display conversation with chat-style left/right bubbles that work in QTextBrowser"""

        html = """
        <html>
        <head>
            <style>
                .msg-container {
                    width: 100%;
                    margin: 6px 0;
                    overflow: auto; /* ensures float clears correctly */
                }
                .user-bubble {
                    float: right;
                    display: block;
                    text-align: right;
                    /*background-color: #E3F2FD;*/
                    color: #000;
                    padding: 10px 14px;
                    border-radius: 12px;
                    max-width: 70%;
                    word-wrap: break-word;
                    margin-left: 40%;
                }
                .bot-bubble {
                    float: left;
                    display: block;
                    text-align: left;
                    /*background-color: #F5F5F5;*/
                    color: #000;
                    padding: 10px 14px;
                    border-radius: 12px;
                    max-width: 70%;
                    word-wrap: break-word;
                    margin-right: 40%;
                }
            </style>
        </head>
        <body style="font-family: Arial; padding: 10px;">
        """

        for role, message in self.conversation_history:
            if role == "user":
                html += f"""
                <div class="msg-container">
                    <div class="user-bubble">{message}</div>
                </div>
                """
            else:
                html += f"""
                <div class="msg-container">
                    <div class="bot-bubble">{message}</div>
                </div>
                """

        html += "</body></html>"

        self.ui.textBrowser_conversation.setHtml(html)

        # Scroll to bottom
        sb = self.ui.textBrowser_conversation.verticalScrollBar()
        sb.setValue(sb.maximum())

    
    def move_then_show(self, x:int, y:int):
        #x and y are coords of buddy_window
        self.move_no_show(x,y)
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
