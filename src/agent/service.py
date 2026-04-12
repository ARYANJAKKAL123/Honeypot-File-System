"""
Honeypot Agent - Windows Service Wrapper
Runs the honeypot agent as a background Windows service

Install:  python src/agent/service.py install
Start:    python src/agent/service.py start
Stop:     python src/agent/service.py stop
Remove:   python src/agent/service.py remove
"""
import sys
import os
import time
import threading

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    import win32serviceutil
    import win32service
    import win32event
    import servicemanager
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
    print("pywin32 not installed. Run: pip install pywin32")

from watchdog.observers import Observer
from src.monitor.file_monitor import FileMonitor
from src.agent.main import load_config


class HoneypotService(win32serviceutil.ServiceFramework if WIN32_AVAILABLE else object):
    """Windows Service wrapper for the Honeypot Agent."""

    _svc_name_ = "HoneypotAgent"
    _svc_display_name_ = "Adaptive Honeypot Security Agent"
    _svc_description_ = "Monitors file system for threats and deploys decoy files."

    def __init__(self, args):
        if WIN32_AVAILABLE:
            win32serviceutil.ServiceFramework.__init__(self, args)
            self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.observer = None
        self.running = False

    def SvcStop(self):
        """Called when service is stopped."""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.running = False
        if self.observer:
            self.observer.stop()

    def SvcDoRun(self):
        """Called when service starts - runs the honeypot."""
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.running = True
        self._run_honeypot()

    def _run_honeypot(self):
        """Core honeypot logic - same as main.py."""
        config = load_config()
        watch_dirs = config.get('monitoring', {}).get('watch_directories', ['test_monitor'])

        # Create directories if needed
        for watch_dir in watch_dirs:
            if not os.path.exists(watch_dir):
                os.makedirs(watch_dir)

        # Start monitoring
        handler = FileMonitor()
        self.observer = Observer()

        for watch_dir in watch_dirs:
            self.observer.schedule(handler, path=watch_dir, recursive=True)

        self.observer.start()

        # Keep running until stopped
        while self.running:
            time.sleep(1)

        self.observer.stop()
        self.observer.join()


if __name__ == '__main__':
    if WIN32_AVAILABLE:
        win32serviceutil.HandleCommandLine(HoneypotService)
    else:
        print("pywin32 is required to run as a Windows service.")
        print("Install it with: pip install pywin32")
        print("\nTo run without service, use: python src/agent/main.py")
