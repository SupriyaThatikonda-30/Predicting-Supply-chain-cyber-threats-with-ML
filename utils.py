
import datetime
import logging
import os
import platform

# Set up logging
LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'system_events.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def format_bytes(bytes_value):
    """
    Convert bytes to a human-readable format (e.g., KB, MB, GB)
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024
    return f"{bytes_value:.2f} PB"

def format_time(timestamp):
    """
    Convert datetime or Unix timestamp to readable string
    """
    if isinstance(timestamp, (int, float)):
        return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(timestamp, datetime.datetime):
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')
    return str(timestamp)

def log_event(message, level="info"):
    """
    Log an event to system_events.log
    """
    if level == "info":
        logging.info(message)
    elif level == "warning":
        logging.warning(message)
    elif level == "error":
        logging.error(message)
    elif level == "critical":
        logging.critical(message)
    else:
        logging.debug(message)

def get_os_info():
    """
    Returns a dictionary with OS and platform details
    """
    return {
        "OS": platform.system(),
        "Version": platform.version(),
        "Release": platform.release(),
        "Machine": platform.machine(),
        "Processor": platform.processor()
    }

def classify_threat(threat_desc):
    """
    Classifies threat description into category
    """
    desc = threat_desc.lower()
    if "usb" in desc:
        return "Unauthorized USB Device"
    elif "remote" in desc or "ransomware" in desc:
        return "Remote Access or Malware"
    elif "eventlog" in desc or "audit failure" in desc:
        return "Security Log Alert"
    elif "network" in desc or "traffic" in desc:
        return "Anomalous Network Activity"
    elif "disk full" in desc:
        return "Disk Capacity Warning"
    else:
        return "Unknown Threat"

def create_log_entry(source, message, threat_type=None):
    """
    Creates a formatted log entry dictionary
    """
    return {
        "source": source,
        "message": message,
        "threat_type": threat_type or classify_threat(message),
        "timestamp": format_time(datetime.datetime.now())
    }
