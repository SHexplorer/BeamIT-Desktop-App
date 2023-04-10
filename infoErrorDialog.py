from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon
from ui_error_dialog import Ui_Dialog

class InfoErrorDialog(Ui_Dialog, QDialog):
    input: str
    def __init__(self, message: str, showRedErrorLabel: bool = True, showUserInputFile: bool = False):
        super(InfoErrorDialog, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon.png'))
        self.show()
        if showRedErrorLabel:
            self.setWindowTitle("ERROR")
        else:
            self.setWindowTitle("INFO")
        #self.image = None

        self.l_info: QLabel = self.findChild(QLabel, "l_appname")
        if not showRedErrorLabel:
            self.l_info.hide()
        self.te_input: QTextEdit = self.findChild(QTextEdit, "te_input")
        if not showUserInputFile:
            self.te_input.hide()
        self.l_info: QLabel = self.findChild(QLabel, "l_errormessage")
        self.l_info.setText(message)
        self.b_confirm: QPushButton = self.findChild(QPushButton, "b_confirm")
        self.b_confirm.clicked.connect(self.b_confirm_handler)

    def b_confirm_handler(self):
        self.input = self.te_input.toPlainText()
        self.close()