from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QPushButton, QLineEdit, QMessageBox)

from os import path
import sqlite3
import sys


from application_states import ApplicationStates
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, HEADER_WIDTH, HEADER_HEIGHT,
                       MAIN_MENU_BUTTON_WIDTH, BUTTON_WIDTH, BUTTON_HEIGHT, ENTRY_WIDTH,
                       ENTRY_HEIGHT, USER_BUTTON_WIDTH, USER_BUTTON_HEIGHT)
from database_functions import (add_service, add_user, check_data_from_service, create_database,
                                delete_service, delete_user, get_master_hashed, get_key,
                                get_user_id, get_usernames_list, list_saved_services,
                                update_service_password, update_service_username)
from encryption_functions import get_hash, generate_key, encrypt_password, decrypt_password


class Application(object):
    def __init__(self):
        self.state = ApplicationStates.MAIN_MENU

    def setupUi(self, MainWindow):
        #  Main window setup
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(SCREEN_WIDTH, SCREEN_HEIGHT)
        font = QtGui.QFont()
        font.setPointSize(20)
        MainWindow.setFont(font)
        MainWindow.setFocusPolicy(QtCore.Qt.ClickFocus)
        MainWindow.setStyleSheet("")
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setMinimumSize(QtCore.QSize(SCREEN_WIDTH, SCREEN_HEIGHT))
        MainWindow.setMaximumSize(QtCore.QSize(SCREEN_WIDTH, SCREEN_HEIGHT))

        #  Central widget setup
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #  Header setup
        self.header = QLabel(self.centralwidget)
        font.setPointSize(20)
        self.header.setFont(font)
        self.header.setFocusPolicy(QtCore.Qt.NoFocus)
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.header.setObjectName("header")

        #  ------------------Buttons setup------------------

        #  Sign up button
        self.sign_up_button = QPushButton(self.centralwidget)
        font.setPointSize(16)
        self.sign_up_button.setFont(font)
        self.sign_up_button.clicked.connect(self.sign_up)

        #  Log in button
        self.login_button = QPushButton(self.centralwidget)
        font.setPointSize(16)
        self.login_button.setFont(font)
        MainWindow.setCentralWidget(self.centralwidget)
        self.login_button.clicked.connect(self.login)

        #  Main menu button
        self.main_menu_button = QPushButton(self.centralwidget)
        font.setPointSize(16)
        self.main_menu_button.setFont(font)
        self.main_menu_button.hide()
        self.main_menu_button.clicked.connect(self.main_menu)

        #  Show password button
        self.show_hide_password_button = QPushButton(self.centralwidget)
        font.setPointSize(16)
        self.show_hide_password_button.setFont(font)
        self.show_hide_password_button.hide()
        self.show_hide_password_button.clicked.connect(self.show_password)

        #  Send info button
        self.send_data = QPushButton(self.centralwidget)
        font.setPointSize(16)
        self.send_data.setFont(font)
        self.send_data.hide()
        self.send_data.clicked.connect(self.send)

        #  List saved services button
        self.list_button = QPushButton(self.centralwidget)
        font.setPointSize(12)
        self.list_button.setFont(font)
        self.list_button.hide()
        self.list_button.clicked.connect(self.list)

        #  Add new service button
        self.add_service_button = QPushButton(self.centralwidget)
        font.setPointSize(12)
        self.add_service_button.setFont(font)
        self.add_service_button.hide()
        self.add_service_button.clicked.connect(self.add)

        #  Get data from service button
        self.get_data_button = QPushButton(self.centralwidget)
        font.setPointSize(12)
        self.get_data_button.setFont(font)
        self.get_data_button.hide()
        self.get_data_button.clicked.connect(self.get)

        #  Update service button
        self.update_service_button = QPushButton(self.centralwidget)
        font.setPointSize(12)
        self.update_service_button.setFont(font)
        self.update_service_button.hide()
        self.update_service_button.clicked.connect(self.update)

        #  Delete service button
        self.delete_service_button = QPushButton(self.centralwidget)
        font.setPointSize(12)
        self.delete_service_button.setFont(font)
        self.delete_service_button.hide()
        self.delete_service_button.clicked.connect(self.delete_service)

        #  Delete user button
        self.delete_user_button = QPushButton(self.centralwidget)
        font.setPointSize(12)
        self.delete_user_button.setFont(font)
        self.delete_user_button.hide()
        self.delete_user_button.clicked.connect(self.delete_user)

        #  Logoff user button
        self.logoff_button = QPushButton(self.centralwidget)
        font.setPointSize(12)
        self.logoff_button.setFont(font)
        self.logoff_button.hide()
        self.logoff_button.clicked.connect(self.logoff)

        #  Cancell operation button
        self.cancel_operation_button = QPushButton(self.centralwidget)
        font.setPointSize(16)
        self.cancel_operation_button.setFont(font)
        self.cancel_operation_button.hide()
        self.cancel_operation_button.clicked.connect(self.cancel)

        #  ------------------LineEdit setup------------------

        #  Username
        self.username = QLineEdit(self.centralwidget)
        font.setPointSize(12)
        self.username.setFont(font)
        self.username.hide()
        self.username.setPlaceholderText('Username')

        #  Password
        self.password = QLineEdit(self.centralwidget)
        font.setPointSize(12)
        self.password.setFont(font)
        self.password.hide()
        self.password.setPlaceholderText('Password')

        #  New service name
        self.service_name = QLineEdit(self.centralwidget)
        self.service_name.setFont(font)
        self.service_name.hide()
        self.service_name.setPlaceholderText('Service name')

        #  ------------------Message box setup------------------

        #  Warning box
        self.warning = QMessageBox()
        self.warning.setWindowTitle('Warning!')
        self.warning.setIcon(QMessageBox.Warning)
        self.warning.hide()

        #  Information box
        self.info = QMessageBox()
        self.info.setWindowTitle('Info')
        self.info.setIcon(QMessageBox.Information)
        self.info.hide()

        #  Listing box
        self.listing = QMessageBox()
        self.listing.setWindowTitle('Services list')
        self.listing.setIcon(QMessageBox.Information)
        self.listing.hide()

        #  Delete user box
        self.delete_user = QMessageBox()
        self.delete_user.setWindowTitle('Careful!')
        self.delete_user.setIcon(QMessageBox.Critical)
        self.delete_user.setText(
            'Are you sure you want to do this?\nYou will lose all your passwords!')
        self.delete_user.setStandardButtons(QMessageBox.Yes)
        self.delete_user.buttonClicked.connect(self.delete_user_confirmation)

        self.retranslateUi(MainWindow)
        self.main_menu()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """
        Set texts and titles
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Password manager"))
        self.header.setText(_translate("MainWindow", "MAIN MENU"))
        self.sign_up_button.setText(_translate("MainWindow", "Sign up"))
        self.login_button.setText(_translate("MainWindow", "Log in"))
        self.main_menu_button.setText(_translate('MainWindow', 'Menu'))
        self.show_hide_password_button.setText(
            _translate('MainWindow', 'Show Password'))
        self.send_data.setText(_translate('MainWindow', 'Send'))
        self.list_button.setText('List services')
        self.add_service_button.setText('Add service')
        self.get_data_button.setText('Check password')
        self.update_service_button.setText('Update password')
        self.delete_service_button.setText('Delete service')
        self.delete_user_button.setText('Delete account')
        self.logoff_button.setText('Log-off')
        self.cancel_operation_button.setText('Cancel')

    def reset_widgets(self):
        #  Hide everything
        self.login_button.hide()
        self.sign_up_button.hide()
        self.main_menu_button.hide()
        self.password.hide()
        self.username.hide()
        self.show_hide_password_button.hide()
        self.send_data.hide()
        self.list_button.hide()
        self.add_service_button.hide()
        self.get_data_button.hide()
        self.update_service_button.hide()
        self.delete_service_button.hide()
        self.delete_user_button.hide()
        self.logoff_button.hide()
        self.service_name.hide()
        self.cancel_operation_button.hide()

        #  Clear every QLineEdit
        self.password.clear()
        self.username.clear()
        self.service_name.clear()

        #  Reset every widget geometry
        self.header.setGeometry(
            (SCREEN_WIDTH - HEADER_WIDTH) // 2, SCREEN_HEIGHT // 6, HEADER_WIDTH, HEADER_HEIGHT)
        self.sign_up_button.setGeometry(
            2 * SCREEN_WIDTH // 5 - MAIN_MENU_BUTTON_WIDTH,
            3 * (SCREEN_HEIGHT // 2 - BUTTON_HEIGHT) // 2,
            MAIN_MENU_BUTTON_WIDTH, BUTTON_HEIGHT)
        self.login_button.setGeometry(
            4 * SCREEN_WIDTH // 5 - MAIN_MENU_BUTTON_WIDTH,
            3 * (SCREEN_HEIGHT // 2 - BUTTON_HEIGHT) // 2,
            MAIN_MENU_BUTTON_WIDTH, BUTTON_HEIGHT)
        self.main_menu_button.setGeometry(
            (SCREEN_WIDTH - BUTTON_WIDTH) // 2, 4 * SCREEN_HEIGHT // 5, BUTTON_WIDTH, BUTTON_HEIGHT)
        show_hide_password_button_height = 4 * SCREEN_HEIGHT // 5 - SCREEN_HEIGHT // 10
        self.show_hide_password_button.setGeometry(
            (SCREEN_WIDTH - BUTTON_WIDTH) // 2, show_hide_password_button_height,
            BUTTON_WIDTH, BUTTON_HEIGHT)
        send_data_button_height = show_hide_password_button_height - SCREEN_HEIGHT // 10
        self.send_data.setGeometry(
            (SCREEN_WIDTH - BUTTON_WIDTH) // 2, send_data_button_height,
            BUTTON_WIDTH, BUTTON_HEIGHT)
        self.list_button.setGeometry(
            (SCREEN_WIDTH - 3 * USER_BUTTON_WIDTH) // 2, SCREEN_HEIGHT // 3,
            USER_BUTTON_WIDTH, USER_BUTTON_HEIGHT)
        self.add_service_button.setGeometry(
            (SCREEN_WIDTH - USER_BUTTON_WIDTH) // 2, SCREEN_HEIGHT // 3,
            USER_BUTTON_WIDTH, USER_BUTTON_HEIGHT)
        self.get_data_button.setGeometry(
            (SCREEN_WIDTH + USER_BUTTON_WIDTH) // 2, SCREEN_HEIGHT // 3,
            USER_BUTTON_WIDTH, USER_BUTTON_HEIGHT)
        self.update_service_button.setGeometry(
            (SCREEN_WIDTH - 3 * USER_BUTTON_WIDTH) // 2, SCREEN_HEIGHT // 2,
            USER_BUTTON_WIDTH, USER_BUTTON_HEIGHT)
        self.delete_service_button.setGeometry(
            (SCREEN_WIDTH - USER_BUTTON_WIDTH) // 2, SCREEN_HEIGHT // 2,
            USER_BUTTON_WIDTH, USER_BUTTON_HEIGHT)
        self.delete_user_button.setGeometry(
            (SCREEN_WIDTH + USER_BUTTON_WIDTH) // 2, SCREEN_HEIGHT // 2,
            USER_BUTTON_WIDTH, USER_BUTTON_HEIGHT)
        self.logoff_button.setGeometry(
            (SCREEN_WIDTH - 3 * USER_BUTTON_WIDTH) // 2, 2 * SCREEN_HEIGHT // 3,
            USER_BUTTON_WIDTH * 3, USER_BUTTON_HEIGHT)
        self.cancel_operation_button.setGeometry(
            (SCREEN_WIDTH - BUTTON_WIDTH) // 2, 9 * SCREEN_HEIGHT // 10 - BUTTON_HEIGHT,
            BUTTON_WIDTH, BUTTON_HEIGHT)
        self.username.setGeometry(
            (SCREEN_WIDTH - ENTRY_WIDTH) // 2,  2 * (SCREEN_HEIGHT - ENTRY_HEIGHT) // 5,
            ENTRY_WIDTH, ENTRY_HEIGHT)
        self.password.setGeometry(
            (SCREEN_WIDTH - ENTRY_WIDTH) // 2,  (SCREEN_HEIGHT - ENTRY_HEIGHT) // 2,
            ENTRY_WIDTH, ENTRY_HEIGHT)
        self.service_name.setGeometry(
            (SCREEN_WIDTH - ENTRY_WIDTH) // 2, 29 * (SCREEN_HEIGHT - ENTRY_HEIGHT) // 100,
            ENTRY_WIDTH, ENTRY_HEIGHT)
        self.listing.setGeometry(550, 300, 500, 500)

        #  Hide passwords
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_shown = False

    def sign_up(self):
        """
        Show sign up screen
        """
        self.reset_widgets()
        self.main_menu_button.show()
        self.password.show()
        self.username.show()
        self.show_hide_password_button.show()
        self.send_data.show()
        self.state = ApplicationStates.SIGN_UP
        self.header.setText('Sign up')

    def login(self):
        """
        Show login screen
        """
        self.reset_widgets()
        self.main_menu_button.show()
        self.password.show()
        self.username.show()
        self.show_hide_password_button.show()
        self.state = ApplicationStates.LOGIN
        self.send_data.show()
        self.header.setText('Login')

    def main_menu(self):
        """
        Show main menu screen
        """
        self.reset_widgets()
        self.login_button.show()
        self.sign_up_button.show()
        self.state = ApplicationStates.MAIN_MENU
        self.header.setText('MAIN MENU')

    def show_password(self):
        """
        Toggle passwords is shown on or of
        """
        if self.password_shown:
            self.password.setEchoMode(QLineEdit.Password)
            self.password.EchoMode() == QLineEdit.Password
            self.password_shown = False
            self.show_hide_password_button.setText('Show Password')
        else:
            self.password.setEchoMode(QLineEdit.Normal)
            self.password.EchoMode() == QLineEdit.Normal
            self.password_shown = True
            self.show_hide_password_button.setText('Hide Password')

    def send(self):
        """
        Send data from QLineEdit
        """

        if self.state == ApplicationStates.SIGN_UP:
            self.provided_username = self.username.text()
            self.provided_password = self.password.text()

            if self.provided_username == '' or self.provided_password == '':
                self.warning.setText(
                    'You must type in a username and a password!')
                self.warning.show()
                return

            users_list = get_usernames_list()
            for name in users_list:
                if self.provided_username == name[0]:
                    self.warning.setText('Username alredy taken')
                    self.warning.show()
                    return

            else:
                key = generate_key()
                master_hashed = get_hash(self.provided_password)
                try:
                    add_user(self.provided_username, master_hashed, key)
                    self.info.setText('User registered successully')
                    self.info.show()
                    self.main_menu()
                except sqlite3.Error:
                    self.warning.setText('A problem occurred, try again later')
                    self.warning.show()

        elif self.state == ApplicationStates.LOGIN:

            self.provided_username = self.username.text()
            self.provided_password = self.password.text()

            if self.provided_username == '' or self.provided_password == '':
                self.warning.setText(
                    'You must type in a username and a password!')
                self.warning.show()
                return

            provided_hash = str(get_hash(self.provided_password))

            #  Checking if user exists
            users_list = get_usernames_list()

            for user in users_list:
                if self.provided_username == user[0]:
                    if provided_hash == get_master_hashed(self.provided_username):
                        accessed = True
                        break
                    else:
                        accessed = False
                        break
            else:
                accessed = None

            if accessed:
                self.reset_widgets()
                self.user_id = get_user_id(self.provided_username)
                self.user_key = get_key(self.user_id)
                self.header.setText(f'Welcome {self.provided_username}')
                self.list_button.show()
                self.add_service_button.show()
                self.get_data_button.show()
                self.update_service_button.show()
                self.delete_service_button.show()
                self.delete_user_button.show()
                self.logoff_button.show()

            elif accessed is False:
                self.warning.setText('Access denied!')
                self.warning.show()

            elif accessed is None:
                self.warning.setText('User not found')
                self.warning.show()

        elif self.state == ApplicationStates.ADD_SERVICE:
            service_name = self.service_name.text()
            service_username = self.username.text()
            service_password = self.password.text()

            if service_name == '' or service_username == '' or service_password == '':
                self.warning.setText('All fields are required')
                self.warning.show()
                return

            else:
                services_list = list_saved_services(self.user_id)
                for service in services_list:
                    if service_name == service[0]:
                        self.warning.setText('Service alredy registered')
                        self.warning.show()
                        return

                else:
                    encrypted_password = encrypt_password(
                        self.user_key, service_password)
                    add_service(service_name, service_username,
                                encrypted_password, self.user_id)
                    self.info.setText('Service added successfully')
                    self.info.show()
                    self.cancel()

        elif self.state == ApplicationStates.CHECK_SERVICE:
            service_name = self.service_name.text()

            if service_name == '':
                self.warning.setText('You must type in the service name!')
                self.warning.show()
                return

            services_list = list_saved_services(self.user_id)

            for service in services_list:
                if service_name == service[0]:
                    service_exists = True
                    break
            else:
                service_exists = False

            if not service_exists:
                self.warning.setText('This is not a registered service')
                self.warning.show()

            else:
                username, password = check_data_from_service(
                    self.user_id, service_name)
                password = decrypt_password(self.user_key, password)
                self.info.setText(
                    f'Service: {service[0]}\nUsername: {username}\nPassword: {password}')
                self.info.show()
                self.cancel()

        elif self.state == ApplicationStates.UPDATE_SERVICE:
            service_name = self.service_name.text()
            username = self.username.text()
            password = self.password.text()

            if service_name == '' or (username == '' and password == ''):
                self.warning.setText(
                    'You must choose the service name and at least one of the others!')
                self.warning.show()
                return

            services_list = list_saved_services(self.user_id)

            for name in services_list:
                if name[0] == service_name:
                    service_exists = True
                    break
            else:
                service_exists = False

            if not service_exists:
                self.warning.setText('This is not a registered service')
                self.warning.show()

            else:
                if username == '':
                    encrypted_password = encrypt_password(
                        self.user_key, password)
                    update_service_password(
                        self.user_id, service_name, encrypted_password)

                elif password == '':
                    update_service_username(self.user_id, service_name, username)

                elif username != '' and password != '':
                    encrypted_password = encrypt_password(
                        self.user_key, password)
                    update_service_password(
                        self.user_id, service_name, encrypted_password)
                    update_service_username(
                        self.user_id, service_name, username)

                self.info.setText('Service updated successfully!')
                self.info.show()
                self.cancel()

        elif self.state == ApplicationStates.DELETE_SERVICE:
            service_name = self.service_name.text()

            if service_name == '':
                self.warning.setText('You must type in the service name!')
                self.warning.show()
                return

            services_list = list_saved_services(self.user_id)

            for service in services_list:
                if service_name == service[0]:
                    service_exists = True
                    break
            else:
                service_exists = False

            if not service_exists:
                self.warning.setText('This is not a registered service')
                self.warning.show()

            else:
                delete_service(self.user_id, service_name)
                self.info.setText(
                    f'Service {service_name} was deleted successfully!')
                self.info.show()
                self.cancel()

    def list(self):
        """
        List saved services
        """
        services_list = list_saved_services(self.user_id)
        if len(services_list) == 0:
            self.warning.setText('There are no services yet')
            self.warning.show()
        else:
            text = ''
            for i in range(len(services_list)):
                text += f'Service {i + 1}: {services_list[i][0]}\n'
            self.listing.setText(text)
            self.listing.show()

    def add(self):
        """
        Add new service
        """
        self.reset_widgets()
        self.header.setText('New service')
        self.show_hide_password_button.show()
        self.service_name.show()
        self.username.show()
        self.password.show()
        self.send_data.show()
        self.state = ApplicationStates.ADD_SERVICE
        self.cancel_operation_button.show()

    def get(self):
        """
        Show password checking screen
        """
        self.reset_widgets()
        #  Reset widgets geometry
        self.service_name.setGeometry(
            (SCREEN_WIDTH - ENTRY_WIDTH) // 2, (SCREEN_HEIGHT -
                                                ENTRY_HEIGHT) // 2, ENTRY_WIDTH, ENTRY_HEIGHT
        )
        self.cancel_operation_button.setGeometry(
            (SCREEN_WIDTH - BUTTON_WIDTH) // 2, 4 * SCREEN_HEIGHT // 5 - BUTTON_HEIGHT,
            BUTTON_WIDTH, BUTTON_HEIGHT)
        self.service_name.show()

        #  Reset app state
        self.state = ApplicationStates.CHECK_SERVICE

        #  Show widgets
        self.send_data.show()
        self.cancel_operation_button.show()
        self.header.setText('Password checking')

    def update(self):
        """
        Show service update screen
        """
        self.reset_widgets()
        self.header.setText('Update service')
        self.show_hide_password_button.show()
        self.service_name.show()
        self.username.show()
        self.password.show()
        self.send_data.show()
        self.state = ApplicationStates.UPDATE_SERVICE
        self.cancel_operation_button.show()

    def delete_service(self):
        """
        Show delete service screen
        """
        self.reset_widgets()
        #  Reset widgets geometry
        self.service_name.setGeometry(
            (SCREEN_WIDTH - ENTRY_WIDTH) // 2, (SCREEN_HEIGHT -
                                                ENTRY_HEIGHT) // 2, ENTRY_WIDTH, ENTRY_HEIGHT
        )
        self.cancel_operation_button.setGeometry(
            (SCREEN_WIDTH - BUTTON_WIDTH) // 2, 4 * SCREEN_HEIGHT // 5 - BUTTON_HEIGHT,
            BUTTON_WIDTH, BUTTON_HEIGHT)
        self.service_name.show()

        #  Reset app state
        self.state = ApplicationStates.DELETE_SERVICE

        #  Show widgets
        self.send_data.show()
        self.cancel_operation_button.show()
        self.header.setText('Deleting service')

    def delete_user(self):
        """Show delete user message box"""
        self.delete_user.show()

    def delete_user_confirmation(self):
        """Show delete user confirmation"""
        delete_user(self.user_id)
        self.delete_user.hide()
        self.info.setText('User deleted successfully!')
        self.main_menu()
        self.user_id = None
        self.user_key = None

    def logoff(self):
        """Go to main menu and logoff"""
        self.main_menu()
        self.user_id = None
        self.user_key = None

    def cancel(self):
        """Cancel a operation and return to operation choice menu"""
        self.state = ApplicationStates.LOGIN
        self.reset_widgets()
        self.header.setText(f'Welcome {self.provided_username}')
        self.list_button.show()
        self.add_service_button.show()
        self.get_data_button.show()
        self.update_service_button.show()
        self.delete_service_button.show()
        self.delete_user_button.show()
        self.logoff_button.show()


if __name__ == "__main__":
    if not path.exists('passwords.db'):
        create_database()
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Application()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
