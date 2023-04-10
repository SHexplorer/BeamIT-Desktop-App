# File: main.py
import sys
import os
import platform
import socket
import ctypes
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QFile, QIODevice, QCoreApplication
from PySide6.QtGui import QIcon

import util
from beamit import *
from infoErrorDialog import InfoErrorDialog


beamitsender = beamit_send()
beamitreceiver = beamit_receive()
serverurl = "<-serverurl->"
autoOpen = False
windowstatus = 3
filePath = ""
if platform.system() == "Windows":
    filePath = os.path.expandvars(r'C:/Users/%USERNAME%/Documents/BeamIT')
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('beamit.de')
else:
    filePath = os.path.expandvars(r'/home/$USER/BeamIT')
if socket.gethostname().find('.')>=0:
    devicename=socket.gethostname()
else:
    devicename=socket.gethostbyaddr(socket.gethostname())[0]
returnvalue = None

class SignupPage(QWidget):
    """
    Method to load the UI. 
    """
    def load_ui(self):
        ui_file_name = "Signup-page.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        loader = QUiLoader()
        loader.load(ui_file, self)
        ui_file.close()
    
    def __init__(self):
        super(SignupPage, self).__init__()
        self.load_ui()
        self.setWindowTitle("BeamIT sign up")
        self.setWindowIcon(QIcon('icon.ico'))
        self.image = None

        self.te_username: QTextEdit = self.findChild(QTextEdit, "te_username")
        self.le_password: QLineEdit= self.findChild(QLineEdit, "le_password")
        self.le_repeat_password: QLineEdit= self.findChild(QLineEdit, "le_repeat_password")
        self.te_connection: QTextEdit = self.findChild(QTextEdit, "te_connection")
        self.te_connection.setText(serverurl)

        self.b_confirm: QPushButton = self.findChild(QPushButton, "b_confirm")
        self.b_confirm.clicked.connect(self.b_confirm_handler)
        self.b_confirm_and_sign: QPushButton = self.findChild(QPushButton, "b_confirm_and_sign")
        self.b_confirm_and_sign.clicked.connect(self.b_confirm_and_sign_handler)
        self.b_redirect_login: QPushButton = self.findChild(QPushButton, "b_redirect_login")
        self.b_redirect_login.clicked.connect(self.b_redirect_login_handler)

    """
    Method to check the password and password repeat input. Then confirm the SignUp.
    """
    def b_confirm_handler(self):
        if self.le_password.text() == self.le_repeat_password.text():
            beamitsender.server_url = self.te_connection.toPlainText()
            response = beamitsender.register(self.te_username.toPlainText(), self.le_password.text())

            if response['successfull'] != True:
                self.error = InfoErrorDialog(response['message'])
                self.error.exec()
                app.exit(2)
            else:
                self.info = InfoErrorDialog(response['message'], showRedErrorLabel=False)
                self.info.exec()
        else:
            self.error = InfoErrorDialog("Passwords are not identical")
            self.error.exec()
    
    """
    Method to check the password and password repeat input. Then confirm the SignUp and LogIn.
    """
    def b_confirm_and_sign_handler(self):
        if self.le_password.text() == self.le_repeat_password.text():
            beamitsender.server_url = self.te_connection.toPlainText()
            response = beamitsender.register(self.te_username.toPlainText(), self.le_password.text())

            if response['successfull'] != True:
                self.error = InfoErrorDialog(response['message'])
                self.error.exec()
                app.exit(2)
            else:
                self.info = InfoErrorDialog(response['message'], showRedErrorLabel=False)
                self.info.exec()
                try:
                    response = beamitsender.login(url=self.te_connection.toPlainText(), username=self.te_username.toPlainText(), password=self.le_password.text(), devicename=devicename)
                    if response['successfull'] != True:
                        self.error = InfoErrorDialog(response['message'])
                        self.error.exec()
                    else:
                        accessToken = response['message']
                        util.storeConfig(serverurl=self.te_connection.toPlainText(), username=accessToken['username'], devicename=accessToken['devicename'], devicetoken=accessToken['token'], filepath=filePath, autoOpen=False)
                        app.exit(3)
                except Exception as e:
                    print(e)
                    self.error = InfoErrorDialog("Connection could not be established")
                    self.error.exec()
        else:
            self.error = InfoErrorDialog("Passwords are not identical")
            self.error.show()


    def b_redirect_login_handler(self):
        app.exit(1)
        

class LoginPage(QWidget):
    """
    Method to load the UI.
    """
    def load_ui(self):
        ui_file_name = "LoginPage.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        loader = QUiLoader()
        loader.load(ui_file, self)
        ui_file.close()
     
    def __init__(self):
        super(LoginPage, self).__init__()
        self.load_ui()
        self.setWindowTitle("BeamIT Login")
        self.setWindowIcon(QIcon('icon.ico'))
        self.image = None


        self.b_confirm: QPushButton = self.findChild(QPushButton, "b_confirm")
        self.b_confirm.clicked.connect(self.b_confirm_handler)
        self.b_redirect_signup: QPushButton = self.findChild(QPushButton, "b_redirect_signup")
        self.b_redirect_signup.clicked.connect(self.b_redirect_signup_handler)
        self.te_connection_input: QTextEdit = self.findChild(QTextEdit, "te_connection_input")
        self.te_connection_input.setText(serverurl)

        self.te_username: QTextEdit = self.findChild(QTextEdit, "te_username")
        self.le_password: QLineEdit= self.findChild(QLineEdit, "le_password")

    """
    Method to check the username and password.
    """
    def b_confirm_handler(self):
        try:
            response = beamitsender.login(url=self.te_connection_input.toPlainText(), username=self.te_username.toPlainText(), password=self.le_password.text(), devicename=devicename)
            if response['successfull'] != True:
                self.error = InfoErrorDialog(response['message'])
                self.error.exec()
                app.exit(1)
            else:
                accessToken = response['message']
                util.storeConfig(serverurl=self.te_connection_input.toPlainText(), username=accessToken['username'], devicename=accessToken['devicename'], devicetoken=accessToken['token'], filepath=filePath, autoOpen=False)
                app.exit(3)
        except Exception as e:
            print(e)
            self.error = InfoErrorDialog("Connection could not be established")
            self.error.exec()
        
    def b_redirect_signup_handler(self):
        app.exit(2)
        

class MainWindow(QWidget):
    """
    Method to load the UI.
    """
    def load_ui(self):
        ui_file_name = "mainwindow_v2.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        loader = QUiLoader()
        loader.load(ui_file, self)
        ui_file.close()

    def __init__(self):
        super().__init__()
        self.load_ui()
        self.setWindowTitle("BeamIT Main")
        self.setWindowIcon(QIcon('icon.ico'))
        self.getGuiElements()
        self.setAcceptDrops(True)

    """
    Method to get the other GUI elements. 
    """
    def getGuiElements(self):
        self.b_refresh: QPushButton = self.findChild(QPushButton, "b_refresh")
        self.b_refresh.clicked.connect(self.b_refresh_handler)
        self.lw_devices: QListWidget = self.findChild(QListWidget, "lw_devices")
        
        self.b_delete_device: QPushButton = self.findChild(QPushButton, "b_delete_device")
        self.b_delete_device.clicked.connect(self.b_delete_device_handler)
        self.b_rename_current_device: QPushButton = self.findChild(QPushButton, "b_rename_current_device")
        self.b_rename_current_device.clicked.connect(self.b_rename_current_device_handler)

        self.b_locate_files: QPushButton = self.findChild(QPushButton, "b_locate_files")
        self.b_locate_files.clicked.connect(self.b_locate_files_handler)
        self.l_dragdrop: QLabel = self.findChild(QLabel, "l_dragdrop")

        self.cb_auto_open: QCheckBox = self.findChild(QCheckBox, "cb_auto_open")
        if config['autoOpen'] == "True":
            self.cb_auto_open.setChecked(True)
        elif config['autoOpen'] == "False":
            self.cb_auto_open.setChecked(False)
        self.cb_auto_open.stateChanged.connect(self.cb_auto_open_changed)

        self.b_set_path: QPushButton = self.findChild(QPushButton, "b_set_path")
        self.b_set_path.clicked.connect(self.b_set_path_handler)
        self.b_delete_account: QPushButton = self.findChild(QPushButton, "b_delete_account")
        self.b_delete_account.clicked.connect(self.b_delete_account_handler)
        self.b_logout: QPushButton = self.findChild(QPushButton, "b_logout")
        self.b_logout.clicked.connect(self.b_logout_handler)

    """
    Method to load the devices from the associated user.
    """
    def loadDevices(self):
        self.lw_devices.clear()
        response = beamitsender.listDevices()
        if response['successfull'] == True:
            for device in response['message']:
                self.lw_devices.addItem(QListWidgetItem(device))
        else:
            self.info = InfoErrorDialog(message=response['message'], showRedErrorLabel=True)

    def b_refresh_handler(self):
        self.loadDevices()

    """
    Method to delete the devices from the associated user.
    """
    def b_delete_device_handler(self):
        if self.lw_devices.currentItem():
            if not self.lw_devices.currentItem().text() == config['devicename']:
                response = beamitsender.removeDevice(self.lw_devices.currentItem().text())
                if response['successfull']:
                    self.info = InfoErrorDialog(message=response['message'], showRedErrorLabel=False)
                else:
                    self.info = InfoErrorDialog(message=response['message'], showRedErrorLabel=True)
                self.loadDevices()
            else:
                self.error = InfoErrorDialog("Can not delete own device. Use logout instead")
                self.error.exec()
        else:
            self.error = InfoErrorDialog("No target device selected")
            self.error.exec()
        
    """
    Method to rename the device with which you are logged in.
    """
    def b_rename_current_device_handler(self):
        self.info = InfoErrorDialog(message="Enter new device name", showRedErrorLabel=False, showUserInputFile=True)
        self.info.exec()
        newDeviceName = self.info.input
        response = beamitsender.renameDevices(newDeviceName)
        if response['successfull']:
            self.info = InfoErrorDialog(message=response['message'], showRedErrorLabel=False)
            util.storeConfig(serverurl=serverurl, username=config['username'], devicename=newDeviceName, devicetoken=config['devicetoken'], filepath=filePath, autoOpen=config['autoOpen'])
            beamitsender.devicename=newDeviceName
        else:
            self.info = InfoErrorDialog(message=response['message'], showRedErrorLabel=True)
        self.loadDevices()

    #TODO wird nicht im richtigen ordner geöffnet
    def b_locate_files_handler(self):
        print(filePath)
        util.startfile(path=filePath, filename="", args="explore")

    """
    Methods to get the Drag&Drop-Functionality.
    """
    def dragEnterEvent(self, event):
        if event.answerRect().intersects(self.l_dragdrop.geometry()):
            event.acceptProposedAction()
        
    def dropEvent(self, event):
        if self.lw_devices.currentItem():
            if event.mimeData().text().startswith(("https://", "http://", "www.")):
                response = beamitsender.beamitShare(targetDevices=("{" + self.lw_devices.currentItem().text() + "}"), autoOpen=False, encrypted=False, datatype="url", senddata=event.mimeData().text())
                if not response['successfull']:
                    self.error = InfoErrorDialog(message=response['message'])
                    self.error.show()
            elif event.mimeData().text().startswith(("file:///", '/')):
                filename, filecontent = util.getFile(event.mimeData().text())
                response = beamitsender.beamitShare(targetDevices=("{" + self.lw_devices.currentItem().text() + "}"), autoOpen=False, encrypted=False, datatype="files", senddata=(filename, filecontent))
                if not response['successfull']:
                    self.error = InfoErrorDialog(message=response['message'])
                    self.error.show()
            else:
                response = beamitsender.beamitShare(targetDevices=("{" + self.lw_devices.currentItem().text() + "}"), autoOpen=False, encrypted=False, datatype="text", senddata=event.mimeData().text())
                if not response['successfull']:
                    self.error = InfoErrorDialog(message=response['message'])
                    self.error.show()
        else:
            self.error = InfoErrorDialog("No target device selected")
            self.error.exec()

    def cb_auto_open_changed(self):
        if self.cb_auto_open.checkState() == self.cb_auto_open.checkState().Checked:
            beamitreceiver.autoOpen = True
            util.storeConfig(serverurl=serverurl, username=config['username'], devicename=config['devicename'], devicetoken=config['devicetoken'], filepath=filePath, autoOpen=True)
        else:
            beamitreceiver.autoOpen = False
            util.storeConfig(serverurl=serverurl, username=config['username'], devicename=config['devicename'], devicetoken=config['devicetoken'], filepath=filePath, autoOpen=False)

    #TODO how detect if closed or confirmed path?
    def b_set_path_handler(self):
        self.pathdialog = QFileDialog()
        self.pathdialog.setFileMode(QFileDialog.FileMode.Directory)
        self.pathdialog.exec()
        filePath = self.pathdialog.selectedFiles()[0]
        beamitreceiver.filePath = filePath
        util.storeConfig(serverurl=serverurl, username=config['username'], devicename=config['devicename'], devicetoken=config['devicetoken'], filepath=filePath)
        self.info = InfoErrorDialog("Path changed to " + filePath, showRedErrorLabel=False)
        self.info.exec()
        
    """
    Method to delete the account with which you are logged in.
    """
    def b_delete_account_handler(self):
        self.delete_account_dialog = QMessageBox()
        self.delete_account_dialog.setWindowTitle("Delete Account?")
        self.delete_account_dialog.setText("Do you really want to delete your Account from Server?")
        self.delete_account_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        button = self.delete_account_dialog.exec()

        if button == QMessageBox.Yes:
            response = beamitsender.unregister()
            if response['successfull']:
                self.info = InfoErrorDialog(message=response['message'], showRedErrorLabel=False)
                self.info.exec()
                app.exit(1)
            else:
                self.info = InfoErrorDialog(message=response['message'], showRedErrorLabel=True)
                self.info.exec()

    """
    Method to logout from the device.
    """
    def b_logout_handler(self):
        response = beamitsender.removeDevice(devicename)
        if response['successfull']:
            self.info = InfoErrorDialog("User logged out successfully", showRedErrorLabel=False)
            self.info.exec()
            util.removeConfig()
            app.exit(1)
        else:
            self.info = InfoErrorDialog(message=response['message'], showRedErrorLabel=True)
            self.info.exec()


if __name__ == "__main__":
    if sys.argv[1]:
        os.chdir(sys.argv[1])

    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication()

    while (1):
        if windowstatus == 0: # Exit Application
            sys.exit()

        if windowstatus == 1: # Login screen
            loginpage = LoginPage()
            loginpage.show()
            windowstatus = app.exec()
            loginpage.close()
        
        if windowstatus == 2: # Signup screen
            signuppage = SignupPage()
            signuppage.show()
            windowstatus = app.exec()
            signuppage.close()

        if windowstatus == 3: # Main screen
            config = util.getConfig()
            if config:
                mainWindow = MainWindow()
                beamitsender.init(config['serverurl'], config['username'], config['devicename'], config['devicetoken'])
                filePath = config['filepath']
                devicename = config['devicename']
                serverurl = config['serverurl']
                try:
                    response = beamitsender.listDevices()
                    if response['successfull']:
                        util.createFolder(filePath)
                        mainWindow.show()
                        mainWindow.loadDevices()
                        beamitreceiver.init(config['serverurl'], config['username'], config['devicename'], config['devicetoken'], filePath, autoOpen=config['autoOpen'])
                    
                        beamitreceiver.start()
                        windowstatus = app.exec()
                        mainWindow.close()
                        beamitreceiver.stop()
                    else:
                        error = InfoErrorDialog(message=response['message'])
                        error.show()
                        error.exec()
                        windowstatus = 1
                except Exception as e:
                    print(e)
                    windowstatus = 1

                    delete_account_dialog = QMessageBox()
                    delete_account_dialog.setWindowTitle("Server not reachable")
                    delete_account_dialog.setText("The Server " + serverurl + " is not reachable. Do you want to logout?")
                    delete_account_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    button = delete_account_dialog.exec()

                    if button == QMessageBox.Yes:
                        util.removeConfig()
                        windowstatus=1
            else:
                windowstatus = 1