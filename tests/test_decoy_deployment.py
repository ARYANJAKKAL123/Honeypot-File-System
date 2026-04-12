from pathlib import Path
from src.monitor.decoy_manager import DecoyManager
from src.monitor.file_monitor import FileMonitor


def test_decoy_manager_deploys_for_suspicious_threat(tmp_path):
    manager = DecoyManager(decoy_base_path=str(tmp_path / "decoys"))
    trigger_file = tmp_path / "notes.txt"

    deployed = manager.deploy_for_threat(
        threat_score=60,
        threat_level="Suspicious",
        trigger_path=str(trigger_file),
    )

    assert deployed is not None
    assert len(deployed) == 2
    assert all(Path(decoy.file_path).exists() for decoy in deployed)


def test_decoy_manager_deduplicates_deployments(tmp_path):
    manager = DecoyManager(decoy_base_path=str(tmp_path / "decoys"))
    trigger_file = tmp_path / "passwords.txt"

    first = manager.deploy_for_threat(
        threat_score=75,
        threat_level="Critical",
        trigger_path=str(trigger_file),
    )
    second = manager.deploy_for_threat(
        threat_score=80,
        threat_level="Critical",
        trigger_path=str(trigger_file),
    )

    assert len(first) == 4
    assert second is None  # duplicate deployment blocked
    assert manager.decoys_deployed is True


def test_decoy_manager_does_not_deploy_below_threshold(tmp_path):
    manager = DecoyManager(decoy_base_path=str(tmp_path / "decoys"))
    trigger_file = tmp_path / "normal.txt"

    result = manager.deploy_for_threat(
        threat_score=30,
        threat_level="Normal",
        trigger_path=str(trigger_file),
    )

    assert result is None
    assert manager.decoys_deployed is False


def test_file_monitor_deploys_decoys_on_sensitive_files(tmp_path):
    monitor = FileMonitor()
    monitor.decoy_manager = DecoyManager(decoy_base_path=str(tmp_path / "decoys"))

    class MockEvent:
        def __init__(self, src_path):
            self.src_path = src_path
            self.is_directory = False

    sensitive_files = [
        "passwords.txt", "api_keys.txt", "secret_token.txt",
        "database_config.yaml", "admin_credentials.txt"
    ]
    for f in sensitive_files:
        monitor.on_created(MockEvent(str(tmp_path / f)))

    status = monitor.decoy_manager.get_deployment_status()
    assert status['deployed'] is True
    assert status['count'] >= 2
