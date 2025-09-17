import time
from threading import Lock

# Thread-safe shared state
_lock = Lock()
latest_usb_alert = {}

def update_usb_alert(device, upload_speed, download_speed):
    global latest_usb_alert
    with _lock:
        latest_usb_alert = {
            "device": device,
            "upload_speed": upload_speed,
            "download_speed": download_speed,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
        }

def get_usb_alert():
    with _lock:
        return latest_usb_alert.copy()
