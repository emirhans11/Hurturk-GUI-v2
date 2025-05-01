from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QUrl
import os

class MapWidget(QWidget):
    def __init__(self, parent=None):
        super(MapWidget, self).__init__(parent)

        # WebEngineView ile haritayı göster
        self.browser = QWebEngineView(self)
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "map.html"))
        self.browser.setUrl(QUrl.fromLocalFile(file_path))

        # Tam ekran yap
        self.browser.setGeometry(self.rect())
        self.browser.setZoomFactor(1.2)

        layout = parent.layout()
        if layout is not None:
            layout.addWidget(self.browser)
        else:
            print("Uyarı: MapWidget eklenmeden önce parent layout'u ayarlanmalı.")
    def update_plane(self, lat, lon, yaw):
        js_code = f"updateOurPlane({lat}, {lon}, {yaw});"
        self.browser.page().runJavaScript(js_code)

