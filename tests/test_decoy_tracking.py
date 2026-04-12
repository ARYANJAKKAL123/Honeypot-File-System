from src.monitor.decoy_manager import DecoyManager
from src.monitor.file_monitor import FileMonitor


def test_decoy_manager_tracks_decoy_access(tmp_path):
    manager = DecoyManager(decoy_base_path=str(tmp_path / "decoys"))
    trigger_file = tmp_path / "suspicious_passwords.txt"

    deployed = manager.deploy_for_threat(
        threat_score=75,
        threat_level="Critical",
        trigger_path=str(trigger_file),
    )
    assert len(deployed) == 4

    # Access a deployed decoy
    result = manager.track_decoy_access(
        file_path=deployed[0].file_path,
        event_type="modified",
        threat_level="Critical",
        threat_score=82,
    )

    assert result is True
    # Attack should be recorded
    stats = manager.get_attack_statistics()
    assert stats['total_attacks'] == 1
    assert stats['attacks'][0]['event_type'] == "modified"
    assert stats['attacks'][0]['threat_level'] == "Critical"


def test_decoy_manager_ignores_non_decoy_files(tmp_path):
    manager = DecoyManager(decoy_base_path=str(tmp_path / "decoys"))

    result = manager.track_decoy_access(
        file_path=str(tmp_path / "normal_file.txt"),
        event_type="modified",
        threat_level="Normal",
        threat_score=10,
    )

    assert result is False
    stats = manager.get_attack_statistics()
    assert stats['total_attacks'] == 0


def test_file_monitor_detects_decoy_access(tmp_path):
    monitor = FileMonitor()
    monitor.decoy_manager = DecoyManager(decoy_base_path=str(tmp_path / "decoys"))

    trigger_file = tmp_path / "password_seed.txt"
    deployed = monitor.decoy_manager.deploy_for_threat(
        threat_score=60,
        threat_level="Suspicious",
        trigger_path=str(trigger_file),
    )
    assert len(deployed) == 2

    class MockEvent:
        def __init__(self, src_path):
            self.src_path = src_path
            self.is_directory = False

    # Simulate attacker touching a deployed decoy
    monitor.on_modified(MockEvent(deployed[0].file_path))

    stats = monitor.decoy_manager.get_attack_statistics()
    assert stats['total_attacks'] >= 1
