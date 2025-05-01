from PyQt5.QtCore import QThread, pyqtSignal
from functions import get_imu_data
import time

class IMUWorker(QThread):
    imu_data_signal = pyqtSignal(dict)

    def run(self):
        while True:
            data, status = get_imu_data()
            if status == 200 and data:
                self.imu_data_signal.emit(data)
            else:
                self.imu_data_signal.emit({})
            time.sleep(1)

class IMUController:
    def __init__(self, ui=None, hud=None, terminal_log=None):
        self.ui = ui
        self.hud = hud
        self.terminal_log = terminal_log
        self.angles = {"pitch": 0, "roll": 0, "yaw": 0}

        self.worker = IMUWorker()
        self.worker.imu_data_signal.connect(self.update_ui)
        self.worker.start()

    def update_ui(self, data):
        if data:
            pitch = data.get("pitch", 0)
            roll = data.get("roll", 0)
            yaw = data.get("yaw", 0)

            self.angles["pitch"] = pitch
            self.angles["roll"] = roll
            self.angles["yaw"] = yaw

            if self.ui:
                self.ui.lbl_pitch.setText(str(pitch))
                self.ui.lbl_roll.setText(str(roll))
                self.ui.lbl_yaw.setText(str(yaw))

            if self.hud:
                self.hud.setPitch(pitch)
                self.hud.setRoll(roll)
                self.hud.setYaw(yaw)

        else:
            if self.terminal_log:
                self.terminal_log("[HATA] IMU verisi alınamadı.")
            if self.ui:
                self.ui.lbl_pitch.setText("N/A")
                self.ui.lbl_roll.setText("N/A")
                self.ui.lbl_yaw.setText("N/A")

    def get_yaw(self):
        return self.angles.get("yaw", 0)
