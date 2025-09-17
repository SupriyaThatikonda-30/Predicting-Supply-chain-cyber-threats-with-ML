import psutil
from flask import Blueprint, jsonify
from app.services.usb_alert import get_usb_alert  # Use getter for thread-safe access

api_bp = Blueprint('api_bp', __name__, url_prefix='/api')

@api_bp.route('/health')
def api_health():
    health = {
        "cpu": f"{psutil.cpu_percent()}% usage",
        "ram": f"{psutil.virtual_memory().percent}% usage",
        "disk": f"{psutil.disk_usage('/').percent}% used"
    }
    return jsonify(health)

@api_bp.route('/cpu_usage')
def api_cpu_usage():
    # Return real-time CPU percent as JSON
    cpu_percent = psutil.cpu_percent(interval=1)
    return jsonify({'cpu': cpu_percent})

@api_bp.route('/usb_alert')
def api_usb_alert():
    # Return latest USB alert info as JSON (thread-safe)
    return jsonify(get_usb_alert())


from app.services.network_monitor import get_network_state

@api_bp.route('/network/speed')
def api_network_speed():
    """Return real-time upload/download speed and totals."""
    return jsonify(get_network_state())
