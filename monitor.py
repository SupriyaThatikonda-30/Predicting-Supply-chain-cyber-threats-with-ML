import time
import socket
import getpass
from app.services.emailer import send_email
from app.services.usb_alert import update_usb_alert
import pythoncom
import wmi

def who_and_where():
    try:
        username = getpass.getuser()
    except Exception:
        username = "Unknown User"
    try:
        hostname = socket.gethostname()
    except Exception:
        hostname = "Unknown Host"
    try:
        ip_addr = socket.gethostbyname(hostname)
    except Exception:
        ip_addr = "Unknown IP"
    return username, hostname, ip_addr

def monitor_usb_devices():
    # Initialize COM for this thread (required for WMI)
    pythoncom.CoInitialize()

    print("[INFO] USB monitoring thread started.")

    c = wmi.WMI()
    known_devices = set(d.DeviceID for d in c.Win32_LogicalDisk())

    # Simulate a new device detection after 10 seconds
    time.sleep(10)
    new_devices = {'Z:'}  # Simulated new device drive letter

    username, hostname, ip_addr = who_and_where()

    for device in new_devices:
        subject = "⚠ Unauthorized USB Device Detected"
        body = f"""🚨 Device Access Alert
A new USB device was connected.

Device: {device}
User: {username}
Hostname: {hostname}
IP Address: {ip_addr}
Time: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""
        # Update shared state for dashboard alert
        update_usb_alert(device=device, upload_speed=None, download_speed=None)
        # Send email
        send_email(subject, body)
        print(body)
