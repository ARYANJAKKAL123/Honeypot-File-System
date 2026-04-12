"""
Honeypot Agent - Main Entry Point
Loads config and starts file system monitoring
"""
import os
import sys
import time
import yaml
from watchdog.observers import Observer

# Add src to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.monitor.file_monitor import FileMonitor, FileSystemEventHandler


class VerboseFileMonitor(FileMonitor):
    """FileMonitor with console output for live feedback."""

    def _handle_file_event(self, event_type, file_path, event_label):
        # Print to console
        print(f"[EVENT] {event_label}: {file_path}")
        # Call parent (does logging + threat detection + decoy logic)
        super()._handle_file_event(event_type, file_path, event_label)
        # Print threat score after each event
        score = self.threat_detector.threat_score
        level = self.threat_detector.get_threat_level()
        if score >= 31:
            print(f"  ⚠️  Threat: {level} (Score: {score})")
        if score >= 51:
            print(f"  🚨 DECOYS DEPLOYED!")


def load_config(config_path="config/config.yaml"):
    """Load configuration from YAML file."""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Config file not found: {config_path}. Using defaults.")
        return {
            'agent': {'name': 'honeypot-agent-01', 'log_level': 'INFO'},
            'monitoring': {'watch_directories': ['test_monitor']}
        }


def main():
    """Main entry point - starts the honeypot agent."""
    print("=" * 50)
    print("  Adaptive File System Honeypot Agent")
    print("=" * 50)

    # Load config
    config = load_config()
    agent_name = config.get('agent', {}).get('name', 'honeypot-agent-01')
    watch_dirs = config.get('monitoring', {}).get('watch_directories', ['test_monitor'])

    print(f"Agent: {agent_name}")
    print(f"Watching: {watch_dirs}")
    print("-" * 50)

    # Create watch directories if they don't exist
    for watch_dir in watch_dirs:
        if not os.path.exists(watch_dir):
            os.makedirs(watch_dir)
            print(f"Created watch directory: {watch_dir}")

    # Set up monitor and observer
    handler = VerboseFileMonitor()
    observer = Observer()

    for watch_dir in watch_dirs:
        observer.schedule(handler, path=watch_dir, recursive=True)
        print(f"Monitoring: {watch_dir}")

    # Start monitoring
    observer.start()
    print("\nHoneypot is ACTIVE. Press Ctrl+C to stop.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down honeypot agent...")
        observer.stop()

    observer.join()
    print("Honeypot agent stopped.")


if __name__ == "__main__":
    main()
