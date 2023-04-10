# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'error_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QPushButton,
    QSizePolicy, QTextEdit, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(371, 202)
        Dialog.setStyleSheet(u"background-color: rgb(27, 29, 35);")
        self.l_background = QLabel(Dialog)
        self.l_background.setObjectName(u"l_background")
        self.l_background.setGeometry(QRect(0, 0, 371, 201))
        self.l_background.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 115, 255,100), stop:1 rgba(0, 0, 0, 200));\n"
"border-radius:15px;")
        self.l_appname = QLabel(Dialog)
        self.l_appname.setObjectName(u"l_appname")
        self.l_appname.setGeometry(QRect(10, 10, 351, 31))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.l_appname.setFont(font)
        self.l_appname.setAutoFillBackground(False)
        self.l_appname.setStyleSheet(u"background-color:rgba(0, 0, 0, 0);\n"
"\n"
"border:none;\n"
"border-bottom:2px solid rgba(255, 0, 4, 230);\n"
"color:rgba(255, 0, 4, 230);\n"
"\n"
"padding-bottom:7px;")
        self.l_appname.setAlignment(Qt.AlignCenter)
        self.l_errormessage = QLabel(Dialog)
        self.l_errormessage.setObjectName(u"l_errormessage")
        self.l_errormessage.setGeometry(QRect(10, 50, 351, 71))
        font1 = QFont()
        font1.setPointSize(10)
        self.l_errormessage.setFont(font1)
        self.l_errormessage.setAutoFillBackground(False)
        self.l_errormessage.setStyleSheet(u"background-color:rgba(0, 0, 0, 0);\n"
"border:none;\n"
"\n"
"color:rgba(255, 255, 255, 230);\n"
"padding-bottom:7px;")
        self.l_errormessage.setAlignment(Qt.AlignCenter)
        self.l_errormessage.setWordWrap(True)
        self.b_confirm = QPushButton(Dialog)
        self.b_confirm.setObjectName(u"b_confirm")
        self.b_confirm.setGeometry(QRect(130, 160, 111, 31))
        self.b_confirm.setFont(font1)
        self.b_confirm.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.te_input = QTextEdit(Dialog)
        self.te_input.setObjectName(u"te_input")
        self.te_input.setGeometry(QRect(20, 120, 331, 31))
        self.te_input.setStyleSheet(u"background-color:rgba(0, 0, 0, 80);\n"
"border:none;\n"
"\n"
"color:rgba(255, 255, 255, 100);\n"
"padding-bottom:7px;")

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis(QCoreApplication.translate("Dialog", u"<html><head/><body><p>background-color: rgb(27, 29, 35);</p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.l_background.setText("")
        self.l_appname.setText(QCoreApplication.translate("Dialog", u"Error", None))
        self.l_errormessage.setText(QCoreApplication.translate("Dialog", u"<ErrorMessage>", None))
        self.b_confirm.setText(QCoreApplication.translate("Dialog", u"Confirm", None))
    # retranslateUi

