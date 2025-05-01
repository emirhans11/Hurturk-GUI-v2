
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPolygon, QPixmap
from PyQt5.QtCore import QPoint, Qt
import math

class HudWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(320, 320)
        self.setStyleSheet("background: transparent;")

        self.pitch = 0
        self.roll = 0
        self.yaw = 0

        # === GÖRSELLERİ YÜKLE ===
        self.pitch_bar = QPixmap("icons/pitch_bar.png").scaled(100, 900, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.roll_bar = QPixmap("icons/roll_bar.png").scaled(280, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.yaw_strip = QPixmap("icons/yaw_tick.png").scaled(600, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Sabit merkez ok
        self.lb_arrow = QLabel(self)
        self.lb_arrow.setPixmap(QPixmap("icons/down-arrow.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.lb_arrow.setGeometry(140, 140, 40, 40)
        self.lb_arrow.setStyleSheet("background-color: transparent;")

        # ARM yazısı
        self.lb_arm = QLabel(self)
        self.lb_arm.setGeometry(10, 295, 100, 20)
        self.lb_arm.setFont(QFont("Arial", 10))
        self.lb_arm.setStyleSheet("color: white; background-color: transparent;")
        self.lb_arm.setText("DISARMED")

        # Bağlantı ikonları
        self.lb_conn_icon = QLabel(self)
        self.lb_conn_icon.setPixmap(QPixmap("icons/high_connection.png").scaled(20, 20))
        self.lb_conn_icon.setGeometry(285, 292, 20, 20)
        self.lb_conn_icon.setStyleSheet("background-color: transparent;")

        self.lb_conn_text = QLabel(self)
        self.lb_conn_text.setGeometry(245, 292, 40, 20)
        self.lb_conn_text.setFont(QFont("Arial", 10))
        self.lb_conn_text.setStyleSheet("color: white; background-color: transparent;")
        self.lb_conn_text.setText("98%")

    def setPitch(self, value):
        self.pitch = value
        self.update()

    def setRoll(self, value):
        self.roll = value
        self.update()

    def setYaw(self, value):
        self.yaw = value
        self.update()

    def setArmStatus(self, armed: bool):
        self.lb_arm.setText("ARMED" if armed else "DISARMED")

    def setConnectionLevel(self, level):
        icon = {
            "high": "icons/high_connection.png",
            "medium": "icons/medium_connection.png",
            "low": "icons/low_connection.png"
        }.get(level, "icons/low_connection.png")
        self.lb_conn_icon.setPixmap(QPixmap(icon).scaled(20, 20))

    def setConnectionPercent(self, percent):
        self.lb_conn_text.setText(f"{percent}%")

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # Merkez noktası
        cx, cy = 160, 160

        # Horizon çizgisi için eğim + bias
        slope = math.tan(math.radians(-self.roll))
        bias = cy - slope * cx
        x1, x2 = 0, 320
        y1 = slope * x1 + bias + self.pitch * 2.5
        y2 = slope * x2 + bias + self.pitch * 2.5

        # Horizon çizgisi
        p.setPen(QPen(Qt.black, 2))
        p.drawLine(int(x1), int(y1), int(x2), int(y2))

        # Gökyüzü
        p.setBrush(QColor(41, 119, 239))
        p.setPen(Qt.NoPen)
        sky_poly = QPolygon([
            QPoint(int(x1), int(y1)),
            QPoint(0, 0),
            QPoint(320, 0),
            QPoint(int(x2), int(y2))
        ])
        p.drawPolygon(sky_poly)

        # Zemin
        p.setBrush(QColor(137, 71, 0))
        ground_poly = QPolygon([
            QPoint(int(x1), int(y1)),
            QPoint(0, 320),
            QPoint(320, 320),
            QPoint(int(x2), int(y2))
        ])
        p.drawPolygon(ground_poly)

        # Pitch bar (yukarı/aşağı kayar)
        pitch_offset = int(self.pitch * 2.5)
        p.drawPixmap(110, -290 + pitch_offset, self.pitch_bar)

        # Roll bar (döner)
        roll_center = QPoint(160, 50)
        p.save()
        p.translate(roll_center)
        p.rotate(-self.roll)
        p.translate(-roll_center)
        p.drawPixmap(20, 0, self.roll_bar)
        p.restore()

        # Yaw tick bar (yatay kayar)
        yaw_x = int(160 - (self.yaw - 180) * 1.5)
        p.drawPixmap(yaw_x - 300, 280, self.yaw_strip)

        p.end()
