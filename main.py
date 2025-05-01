from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QLabel, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import sys
from functions import validate_credentials
from gui import AnaPencere
from map import MapWidget
from hud import HudWidget
from PyQt5.QtGui import QIcon


class StyledLoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HÜRTÜRK Giriş Paneli")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: white;")
        self.setWindowIcon(QIcon("icons/team-logo.png"))  # ← ✨ BURAYA EKLE      
        # Logo
        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap("icons/team-logo.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.setWindowIcon(QIcon("icons/hurturk_logo.png"))
        # Başlık
        self.title = QLabel("HÜRTÜRK GİRİŞ PANELİ")
        self.title.setFont(QFont("Arial", 14, QFont.Bold))
        self.title.setStyleSheet("color: red;")
        self.title.setAlignment(Qt.AlignCenter)

        # Giriş alanları
        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Kullanıcı Adı")
        self.input_username.setStyleSheet("""
            padding: 8px;
            border: 2px solid red;
            border-radius: 10px;
            background-color: #fff;
        """)
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setPlaceholderText("Şifre")
        self.input_password.setStyleSheet("""
            padding: 8px;
            border: 2px solid red;
            border-radius: 10px;
            background-color: #fff;
        """)
        # Giriş butonu
        self.login_button = QPushButton("Giriş Yap")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        self.login_button.clicked.connect(self.check_login)
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.logo_label)
        layout.addWidget(self.title)
        layout.addWidget(self.input_username)
        layout.addWidget(self.input_password)
        layout.addWidget(self.login_button)
        layout.setContentsMargins(50, 20, 50, 20)

        self.setLayout(layout)

    def check_login(self):
        username = self.input_username.text()
        password = self.input_password.text()

        if validate_credentials(username, password):
            self.accept_login(username)
        else:
            QMessageBox.warning(self, "Hatalı Giriş", "Kullanıcı adı veya şifre yanlış!")

    def accept_login(self, username):
        self.main_window = AnaPencere()

        map_widget = MapWidget(self.main_window.ui.verticalLayoutWidget_4)
        self.main_window.set_map_widget(map_widget)

        self.main_window.hud = HudWidget()
        self.main_window.ui.vl_HUD.addWidget(self.main_window.hud)
        self.main_window.set_hud(self.main_window.hud)
        self.main_window.set_user_info(username)

        self.main_window.show()
        self.close()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = StyledLoginWindow()
    win.show()
    sys.exit(app.exec_())
