from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
from design import Ui_Taslak
from functions import post_flight_mode, toggle_arm
from imu import IMUController
from gps import GPSController
from PyQt5.QtWidgets import QMessageBox
from functions import get_user_role, get_welcome_message, apply_permissions
from PyQt5.QtGui import QIcon
from camera import CameraWorker
from PyQt5.QtGui import QPixmap, QImage
import functions
class AnaPencere(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Taslak()
        self.ui.setupUi(self)
        self.setWindowTitle("HÜRTÜRK KONTROL ARAYÜZÜ")  # ← ✨ BURAYA
        # HUD başlangıçta tanımlı değilse sorun çıkmasın
        self.hud = None
        self.setWindowIcon(QIcon("icons/team-logo.png"))
        # IMU Controller bağlanıyor
        self.imu = IMUController(
            ui=self.ui,
            hud=self.hud,
            terminal_log=self.terminale_yaz
        )

        self.timer_imu = QTimer()
        # GPS Controller bağlanıyor
        self.gps = GPSController(
            ui=self.ui,
            terminal_log=self.terminale_yaz
        )
        self.ui.pb_server.clicked.connect(self.kaydet_server_ip)

        self.ui.ip_adres_1.setText("127.0.0.1")  # Başlangıç default IP
        self.ui.port_1.setText("5000")           # Başlangıç default port

        self.gps.imu = self.imu  # ← Artık hata vermez çünkü self.imu var ✅
        self.timer_gps = QTimer()
        # Buton bağlantıları
        self.ui.pb_mod_onay.clicked.connect(self.ucus_modu_gonder)
        self.ui.pb_arm.clicked.connect(self.arm_toggle)
        self.ui.pb_kill.clicked.connect(self.terminali_temizle)

        self.armed = False  # Başlangıç durumu
        self.camera_worker = CameraWorker()
        self.camera_worker.frame_ready.connect(self.update_camera_view)
        self.camera_worker.start()

    def set_user_info(self, username):
        self.username = username
        self.role = get_user_role(username)

        msg = get_welcome_message(username, self.role)
        self.terminale_yaz(msg)

        apply_permissions(self.ui, self.role)
    def set_map_widget(self, map_widget):
        self.map_widget = map_widget
        if hasattr(self, "gps"):
            self.gps.map_widget = map_widget

    def set_hud(self, hud):
        self.hud = hud
        self.imu.hud = hud  # IMUController içindeki hud bağlantısını güncelle
    def kaydet_server_ip(self):
        ip = self.ui.ip_adres_1.text().strip()
        port = self.ui.port_1.text().strip()
        
        if ip and port:
            full_url = f"http://{ip}:{port}"
            functions.SERVER_IP = full_url
            self.terminale_yaz(f"[AYAR] Server IP güncellendi: {full_url}")
        else:
            self.terminale_yaz("[UYARI] IP adresi veya port boş bırakılamaz.")
    def terminale_yaz(self, mesaj):
        eski = self.ui.lbl_terminal.text()
        yeni = eski + f"\n{mesaj}"
        self.ui.lbl_terminal.setText(yeni)

    def terminali_temizle(self):
        self.ui.lbl_terminal.setText("")
    def update_camera_view(self, frame):
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(q_img)
        self.ui.lbl_kamera.setPixmap(pixmap.scaled(self.ui.lbl_kamera.width(), self.ui.lbl_kamera.height(), aspectRatioMode=1))

    def ucus_modu_gonder(self):
        mode = self.ui.cb_ucus_mod.currentText().upper()
        cevap, status = post_flight_mode(mode)

        if hasattr(self, "hud") and self.hud:
            self.hud.setArmStatus(mode == "ARM")

        self.terminale_yaz(f"[MOD] {mode} gönderildi | Durum: {status} | Cevap: {cevap}")

    def arm_toggle(self):
        new_mode, cevap, status = toggle_arm(self.armed)
        self.armed = (new_mode == "ARM")
        self.ui.pb_arm.setText("DISARM" if self.armed else "ARM")

        if hasattr(self, "hud") and self.hud:
            self.hud.setArmStatus(self.armed)

        self.terminale_yaz(f"[ARM] {new_mode} komutu gönderildi | Durum: {status} | Cevap: {cevap}")
    def arm_toggle(self):
        new_mode = "DISARM" if self.armed else "ARM"
        onay = QMessageBox.question(
            self,
            f"{new_mode} Onayı",
            f"Uçağı {new_mode} etmek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No
        )
        if onay == QMessageBox.Yes:
            new_mode, cevap, status = toggle_arm(self.armed)
            self.armed = (new_mode == "ARM")
            self.ui.pb_arm.setText("DISARM" if self.armed else "ARM")

            if hasattr(self, "hud") and self.hud:
                self.hud.setArmStatus(self.armed)

            self.terminale_yaz(f"[ARM] {new_mode} komutu gönderildi | Durum: {status} | Cevap: {cevap}")
        else:
            self.terminale_yaz(f"[ARM] {new_mode} komutu kullanıcı tarafından iptal edildi.")