import os
from flask import Flask
from threading import Thread
from app.routes.dashboard import dashboard_bp
from app.routes.logs import logs_bp
from app.routes.api import api_bp
from app.services.monitor import monitor_usb_devices  # USB monitor
from app.services.network_monitor import start_network_monitor

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')

    # Register all blueprints
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(logs_bp)
    app.register_blueprint(api_bp)

    # Start background threads for monitoring
    def start_usb_monitoring():
        monitor_usb_devices()

    def start_net_monitoring():
        start_network_monitor()

    Thread(target=start_usb_monitoring, daemon=True).start()
    Thread(target=start_net_monitoring, daemon=True).start()

    return app
