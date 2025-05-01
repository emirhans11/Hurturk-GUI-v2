import requests
import cv2
SERVER_IP = "http://127.0.0.1:5000"  # Başlangıçta default localhost olsun

def get_camera_frame():
    cap = cv2.VideoCapture(0)  # 0 = Bilgisayarın dahili kamerası
    if not cap.isOpened():
        print("[HATA] Kamera açılamadı.")
        return None

    ret, frame = cap.read()
    cap.release()

    if ret:
        return frame
    else:
        print("[HATA] Kamera görüntüsü alınamadı.")
        return None


def validate_credentials(username, password):
    users = {
        "admin": "1",
        "technician": "techpass",
        "viewer": "viewpass",
    }
    return users.get(username) == password

def post_flight_mode(mode):
    try:
        print(f"[POST] Mode: {mode}")
        response = requests.post(f"{SERVER_IP}/arming", json={"mode": mode})
        print(f"[RESPONSE] Status: {response.status_code}, Body: {response.text}")
        return response.text, response.status_code
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] {e}")
        return str(e), 500

def toggle_arm(current_state):
    new_mode = "DISARM" if current_state else "ARM"
    try:
        print(f"[TOGGLE ARM] Sending {new_mode}")
        response = requests.post(f"{SERVER_IP}/arming", json={"mode": new_mode})
        print(f"[RESPONSE] Status: {response.status_code}, Body: {response.text}")
        return new_mode, response.text, response.status_code
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] {e}")
        return new_mode, str(e), 500
def get_imu_data():
    try:
        response = requests.get(f"{SERVER_IP}/imu", timeout=3)
        if response.status_code == 200:
            return response.json(), 200
        else:
            return {}, response.status_code
    except Exception as e:
        print(f"[HATA] IMU verisi alınamadı: {e}")
        return {}, 500



def get_gps_data():
    try:
        response = requests.get(f"{SERVER_IP}/gps", timeout=3)
        if response.status_code == 200:
            return response.json(), 200
        else:
            return {}, response.status_code
    except Exception as e:
        print(f"[HATA] GPS verisi alınamadı: {e}")
        return {}, 500


def get_user_role(username):
    # Gelecekte veritabanı veya json'dan da çekebilirsin
    if username == "admin":
        return "admin"
    elif username == "technician":
        return "technician"
    else:
        return "viewer"

def get_welcome_message(username, role):
    msg = f"[GİRİŞ] Hoş geldin {username} ({role.upper()})"
    if role == "admin":
        msg += "\n[YETKİ] Tüm kontroller aktif."
    elif role == "technician":
        msg += "\n[YETKİ] Teknik kontroller açık, uçuş kontrolleri kapalı."
    elif role == "viewer":
        msg += "\n[YETKİ] Sadece izleme yetkiniz var."
    return msg

def apply_permissions(ui, role):
    if role == "viewer":
        ui.pb_arm.setEnabled(False)
        ui.pb_mod_onay.setEnabled(False)
    elif role == "technician":
        ui.pb_arm.setEnabled(False)
        ui.pb_mod_onay.setEnabled(True)
    elif role == "admin":
        ui.pb_arm.setEnabled(True)
        ui.pb_mod_onay.setEnabled(True)


