from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import time

class CameraWorker(QThread):
    frame_ready = pyqtSignal(object)

    def run(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("[HATA] Kamera bulunamadı.")
            return

        while True:
            ret, frame = self.cap.read()
            if ret:
                self.frame_ready.emit(frame)
            time.sleep(0.03)  # yaklaşık 30 FPS

    def stop(self):
        self.cap.release()
        self.quit()
        self.wait()
