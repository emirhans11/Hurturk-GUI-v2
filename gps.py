from PyQt5.QtCore import QThread, pyqtSignal
from functions import get_gps_data
import time

class GPSWorker(QThread):
    gps_data_signal = pyqtSignal(dict)

    def run(self):
        while True:
            data, status = get_gps_data()
            if status == 200 and data:
                self.gps_data_signal.emit(data)
            else:
                self.gps_data_signal.emit({})
            time.sleep(1)  # 1 saniyede bir çekiyor

class GPSController:
    def __init__(self, ui=None, terminal_log=None, map_widget=None, imu=None):
        self.ui = ui
        self.terminal_log = terminal_log
        self.map_widget = map_widget
        self.imu = imu

        self.worker = GPSWorker()
        self.worker.gps_data_signal.connect(self.update_ui)
        self.worker.start()

    def update_ui(self, data):
        if data:
            enlem = data.get("lat", 0)
            boylam = data.get("lon", 0)
            irtifa = data.get("alt", 0)

            if self.ui:
                self.ui.lbl_enlem.setText(str(enlem))
                self.ui.lbl_boylam.setText(str(boylam))
                self.ui.lbl_irtifa.setText(str(irtifa))

            if self.map_widget and self.imu:
                yaw = self.imu.get_yaw()
                self.map_widget.update_plane(enlem, boylam, yaw)

        else:
            if self.terminal_log:
                self.terminal_log("[HATA] GPS verisi alınamadı.")
            if self.ui:
                self.ui.lbl_enlem.setText("N/A")
                self.ui.lbl_boylam.setText("N/A")
                self.ui.lbl_irtifa.setText("N/A")
