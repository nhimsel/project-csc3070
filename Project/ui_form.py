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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_Window(object):
    def setupUi(self, Window):
        if not Window.objectName():
            Window.setObjectName(u"Window")
        Window.resize(300, 350)
        self.centralwidget = QWidget(Window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.header = QLabel(self.centralwidget)
        self.header.setObjectName(u"header")
        self.header.setMinimumSize(QSize(0, 36))
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.header)

        self.textEdit_output = QTextEdit(self.centralwidget)
        self.textEdit_output.setObjectName(u"textEdit_output")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_output.sizePolicy().hasHeightForWidth())
        self.textEdit_output.setSizePolicy(sizePolicy)
        self.textEdit_output.setReadOnly(True)

        self.verticalLayout.addWidget(self.textEdit_output)

        self.inputRow = QHBoxLayout()
        self.inputRow.setSpacing(8)
        self.inputRow.setObjectName(u"inputRow")
        self.textEdit_input = QTextEdit(self.centralwidget)
        self.textEdit_input.setObjectName(u"textEdit_input")
        self.textEdit_input.setMinimumSize(QSize(0, 80))

        self.inputRow.addWidget(self.textEdit_input)

        self.sendColumn = QVBoxLayout()
        self.sendColumn.setSpacing(6)
        self.sendColumn.setObjectName(u"sendColumn")
        self.verticalSpacerTop = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.sendColumn.addItem(self.verticalSpacerTop)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(40, 40))

        self.sendColumn.addWidget(self.pushButton)

        self.verticalSpacerBottom = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.sendColumn.addItem(self.verticalSpacerBottom)


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
        self.header.setText(QCoreApplication.translate("Window", u"Chat", None))
        self.textEdit_output.setPlaceholderText(QCoreApplication.translate("Window", u"Buddy response...", None))
        self.textEdit_input.setPlaceholderText(QCoreApplication.translate("Window", u"Type your message here...", None))
        self.pushButton.setText(QCoreApplication.translate("Window", u"Send", None))
    # retranslateUi

