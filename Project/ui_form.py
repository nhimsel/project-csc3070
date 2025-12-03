# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QPushButton,
    QSizePolicy, QStatusBar, QTextBrowser, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_Window(object):
    def setupUi(self, Window):
        if not Window.objectName():
            Window.setObjectName(u"Window")
        Window.resize(400, 500)
        self.centralwidget = QWidget(Window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.textBrowser_conversation = QTextBrowser(self.centralwidget)
        self.textBrowser_conversation.setObjectName(u"textBrowser_conversation")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.textBrowser_conversation.sizePolicy().hasHeightForWidth())
        self.textBrowser_conversation.setSizePolicy(sizePolicy)
        self.textBrowser_conversation.setMinimumSize(QSize(0, 0))

        self.verticalLayout.addWidget(self.textBrowser_conversation)

        self.inputRow = QHBoxLayout()
        self.inputRow.setSpacing(8)
        self.inputRow.setObjectName(u"inputRow")
        self.textEdit_input = QTextEdit(self.centralwidget)
        self.textEdit_input.setObjectName(u"textEdit_input")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.textEdit_input.sizePolicy().hasHeightForWidth())
        self.textEdit_input.setSizePolicy(sizePolicy1)
        self.textEdit_input.setMinimumSize(QSize(0, 48))
        self.textEdit_input.setMaximumSize(QSize(16777215, 80))

        self.inputRow.addWidget(self.textEdit_input)

        self.sendColumn = QVBoxLayout()
        self.sendColumn.setSpacing(6)
        self.sendColumn.setObjectName(u"sendColumn")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(40, 40))

        self.sendColumn.addWidget(self.pushButton)


        self.inputRow.addLayout(self.sendColumn)


        self.verticalLayout.addLayout(self.inputRow)

        Window.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(Window)
        self.statusbar.setObjectName(u"statusbar")
        Window.setStatusBar(self.statusbar)

        self.retranslateUi(Window)

        QMetaObject.connectSlotsByName(Window)
    # setupUi

    def retranslateUi(self, Window):
        Window.setWindowTitle(QCoreApplication.translate("Window", u"Chat", None))
        self.textEdit_input.setPlaceholderText(QCoreApplication.translate("Window", u"Type your message here...", None))
        self.pushButton.setText(QCoreApplication.translate("Window", u"Send", None))
    # retranslateUi

