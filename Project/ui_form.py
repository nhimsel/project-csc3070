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
from PySide6.QtWidgets import (QApplication, QLineEdit, QMainWindow, QSizePolicy,
    QStatusBar, QWidget)

class Ui_Window(object):
    def setupUi(self, Window):
        if not Window.objectName():
            Window.setObjectName(u"Window")
        Window.resize(800, 600)
        self.centralwidget = QWidget(Window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.helloworld = QLineEdit(self.centralwidget)
        self.helloworld.setObjectName(u"helloworld")
        self.helloworld.setGeometry(QRect(330, 270, 181, 71))
        font = QFont()
        font.setPointSize(24)
        self.helloworld.setFont(font)
        self.helloworld.setAutoFillBackground(True)
        self.helloworld.setFrame(False)
        self.helloworld.setReadOnly(True)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(210, 460, 113, 24))
        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_2.setGeometry(QRect(490, 460, 113, 24))
        self.lineEdit_2.setReadOnly(True)
        Window.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(Window)
        self.statusbar.setObjectName(u"statusbar")
        Window.setStatusBar(self.statusbar)

        self.retranslateUi(Window)

        QMetaObject.connectSlotsByName(Window)
    # setupUi

    def retranslateUi(self, Window):
        Window.setWindowTitle(QCoreApplication.translate("Window", u"Window", None))
        self.helloworld.setText(QCoreApplication.translate("Window", u"Hello world!", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("Window", u"say smth", None))
    # retranslateUi

