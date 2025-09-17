import psutil
import os

# Sample function to detect high CPU usage as a potential threat
def detect_high_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > 80:  # Example threshold for high CPU usage
        return "High CPU Usage - Potential Threat Detected!"
    return "System is stable"
