"""
Honeypot Dashboard - Flask Web Application
Real-time monitoring dashboard for the Adaptive Honeypot Agent
"""
import os
import sys
import json
import threading
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from watchdog.observers import Observer

from src.monitor.file_monitor import FileMonitor
from src.agent.main import load_config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'honeypot-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global state shared between monitor and dashboard
state = {
    'threat_score': 0,
    'threat_level': 'Normal',
    'decoys_deployed': False,
    'decoy_count': 0,
    'total_alerts': 0,
    'total_attacks': 0,
    'events': [],
    'alerts': [],
    'decoy_files': [],
    'attack_log': [],
}

MAX_EVENTS = 50
MAX_ALERTS = 20


class DashboardFileMonitor(FileMonitor):
    """FileMonitor that pushes updates to the dashboard via SocketIO."""

    def _handle_file_event(self, event_type, file_path, event_label):
        super()._handle_file_event(event_type, file_path, event_label)

        score = self.threat_detector.threat_score
        level = self.threat_detector.get_threat_level()
        status = self.decoy_manager.get_deployment_status()

        # Build event entry
        event = {
            'time': datetime.now().strftime('%H:%M:%S'),
            'type': event_type,
            'file': os.path.basename(file_path),
            'path': file_path,
            'score': score,
            'level': level,
        }

        # Update global state
        state['threat_score'] = score
        state['threat_level'] = level
        state['decoys_deployed'] = status['deployed']
        state['decoy_count'] = status['count']
        state['decoy_files'] = [
            {
                'name': os.path.basename(d.file_path),
                'path': d.file_path,
                'type': d.decoy_type,
                'created': d.created_at.strftime('%H:%M:%S') if hasattr(d.created_at, 'strftime') else str(d.created_at),
            }
            for d in status['decoys']
        ]

        # Add to events list (keep last 50)
        state['events'].insert(0, event)
        state['events'] = state['events'][:MAX_EVENTS]

        # Check for alerts (decoy access)
        alerts = self.decoy_manager.alert_manager.get_alerts()
        state['total_alerts'] = len(alerts)
        state['alerts'] = [
            {
                'time': a.get('timestamp', ''),
                'level': a.get('level', ''),
                'message': a.get('message', ''),
            }
            for a in alerts[-MAX_ALERTS:]
        ][::-1]

        # Check attack stats
        attack_stats = self.decoy_manager.get_attack_statistics()
        state['total_attacks'] = attack_stats.get('total_attacks', 0)
        state['attack_log'] = [
            {
                'id': a.get('attack_id', ''),
                'time': a.get('timestamp', ''),
                'decoy': os.path.basename(a.get('decoy_path', '')),
                'action': a.get('event_type', ''),
                'level': a.get('threat_level', ''),
                'score': a.get('threat_score', 0),
            }
            for a in attack_stats.get('attacks', [])
        ][::-1]  # newest first

        # Push to all connected dashboard clients
        socketio.emit('update', state)


# Global monitor instance
monitor_handler = None
observer = None


def start_monitor():
    """Start the file system monitor in a background thread."""
    global monitor_handler, observer

    config = load_config()
    watch_dirs = config.get('monitoring', {}).get('watch_directories', ['test_monitor'])

    for d in watch_dirs:
        if not os.path.exists(d):
            os.makedirs(d)

    monitor_handler = DashboardFileMonitor()
    observer = Observer()

    for d in watch_dirs:
        observer.schedule(monitor_handler, path=d, recursive=True)

    # Also monitor the decoys folder to detect attacker access
    decoys_dir = 'decoys'
    if not os.path.exists(decoys_dir):
        os.makedirs(decoys_dir)
    observer.schedule(monitor_handler, path=decoys_dir, recursive=True)
    print(f"Also monitoring decoys folder: {decoys_dir}")

    observer.start()
    print(f"Monitor started on: {watch_dirs}")


@app.route('/')
def index():
    """Serve the dashboard page."""
    return render_template('index.html')


@app.route('/api/status')
def api_status():
    """REST endpoint - current system status."""
    return jsonify(state)


@app.route('/api/events')
def api_events():
    """REST endpoint - recent file events."""
    return jsonify(state['events'])


@app.route('/api/alerts')
def api_alerts():
    """REST endpoint - recent alerts."""
    return jsonify(state['alerts'])


@app.route('/api/reset', methods=['POST'])
def api_reset():
    """Reset the honeypot state for a fresh demo."""
    global monitor_handler
    state['threat_score'] = 0
    state['threat_level'] = 'Normal'
    state['decoys_deployed'] = False
    state['decoy_count'] = 0
    state['total_alerts'] = 0
    state['total_attacks'] = 0
    state['events'] = []
    state['alerts'] = []
    state['decoy_files'] = []
    state['attack_log'] = []

    # Reset the monitor components
    if monitor_handler:
        monitor_handler.threat_detector.events = []
        monitor_handler.threat_detector.threat_score = 0
        monitor_handler.decoy_manager.decoys_deployed = False
        monitor_handler.decoy_manager.decoy_service.deployed_decoys = []
        monitor_handler.decoy_manager.attack_tracker.attacks = []
        monitor_handler.decoy_manager.alert_manager.alerts = []

    socketio.emit('update', state)
    return jsonify({'status': 'reset', 'message': 'System reset successfully'})


@socketio.on('connect')
def on_connect():
    """Send current state when a client connects."""
    emit('update', state)


if __name__ == '__main__':
    # Start monitor in background thread
    monitor_thread = threading.Thread(target=start_monitor, daemon=True)
    monitor_thread.start()

    print("\n" + "=" * 50)
    print("  Honeypot Dashboard")
    print("  Open: http://localhost:5000")
    print("=" * 50 + "\n")

    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
