from flask import Blueprint, render_template

# Create a Blueprint for logs
logs_bp = Blueprint('logs_bp', __name__, url_prefix='/logs')

# Route for viewing system logs
@logs_bp.route('/')
def view_logs():
    # Here you can load real log data or sample logs
    logs = ["Log 1: System started", "Log 2: User logged in", "Log 3: Error detected"]
    return render_template('logs.html', logs=logs)
