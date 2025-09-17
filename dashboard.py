from flask import Blueprint, render_template
from flask import Blueprint, jsonify
import psutil

dashboard_bp = Blueprint('dashboard', __name__)

# Route to serve the dashboard page
@dashboard_bp.route('/')
def dashboard():
    health = {
        'cpu': psutil.cpu_percent(interval=1),
        'memory': psutil.virtual_memory().percent,
        'disk': {part.device: psutil.disk_usage(part.mountpoint).percent for part in psutil.disk_partitions()},
        'upload_kbps': 0,  # Add logic to fetch actual upload speed
        'download_kbps': 0  # Add logic to fetch actual download speed
    }
    return render_template('dashboard.html', health=health)

# API to fetch CPU usage for the chart
@dashboard_bp.route('/api/cpu_usage')
def cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1)  # Gets CPU usage
    return jsonify({'cpu': cpu_percent})
