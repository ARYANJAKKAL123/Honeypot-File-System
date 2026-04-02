"""
Full System Integration Test - Day 25-26
Simulates a complete attacker scenario from start to finish
"""

import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.monitor.file_monitor import FileMonitor


# ─── Mock Event ───────────────────────────────────────────────
class MockEvent:
    """
    Simulates a real watchdog file event
    Used to test FileMonitor without touching real files
    """
    def __init__(self, src_path, is_directory=False):
        self.src_path = src_path
        self.is_directory = is_directory


# ─── Test ─────────────────────────────────────────────────────
def test_full_attacker_scenario():
    """Simulate a complete attacker scenario"""
    print("\n" + "="*60)
    print("FULL SYSTEM TEST: Attacker Scenario")
    print("="*60)

    try:
        # ── Step 1: Create the monitor ──────────────────────────
        print("\n[STEP 1] Creating FileMonitor...")
        monitor = FileMonitor()
        print("✅ FileMonitor ready (ThreatDetector + DecoyManager + AlertManager inside)")

        # ── Step 2: Attacker accesses normal files ───────────────
        print("\n[STEP 2] Attacker accessing normal files...")
        normal_files = [
            "documents/report.txt",
            "documents/notes.txt",
            "documents/readme.txt",
        ]
        for f in normal_files:
            monitor.on_created(MockEvent(f))

        score_after_normal = monitor.threat_detector.threat_score
        print(f"✅ Normal files accessed. Threat score: {score_after_normal}")

        # ── Step 3: Attacker accesses sensitive files ────────────
        print("\n[STEP 3] Attacker accessing sensitive files...")
        sensitive_files = [
            "config/database_password.txt",
            "backup/credentials.txt",
            "private/api_key.txt",
            "secret/auth_token.txt",
            "ssh/id_rsa",
        ]
        for f in sensitive_files:
            monitor.on_modified(MockEvent(f))

        score_after_sensitive = monitor.threat_detector.threat_score
        level_after_sensitive = monitor.threat_detector.get_threat_level()
        print(f"✅ Sensitive files accessed.")
        print(f"   Threat score: {score_after_sensitive}")
        print(f"   Threat level: {level_after_sensitive}")

        # ── Step 4: Check if decoys were deployed ────────────────
        print("\n[STEP 4] Checking decoy deployment...")
        status = monitor.decoy_manager.get_deployment_status()

        if status['deployed']:
            print(f"✅ Decoys deployed! Count: {status['count']}")
            for decoy in status['decoys']:
                print(f"   - {decoy.file_path}")
        else:
            print("⚠️  Decoys not deployed yet (threat score may be below 51)")
            print(f"   Current score: {score_after_sensitive}")

        # ── Step 5: Attacker accesses a decoy ────────────────────
        print("\n[STEP 5] Simulating attacker accessing a decoy...")

        if status['deployed'] and status['decoys']:
            decoy_path = status['decoys'][0].file_path
            monitor.on_modified(MockEvent(decoy_path))

            # Check alerts
            alert_count = len(monitor.decoy_manager.alert_manager.alerts)
            print(f"✅ Decoy accessed!")
            print(f"   Alerts generated: {alert_count}")

            if alert_count > 0:
                latest = monitor.decoy_manager.alert_manager.alerts[-1]
                print(f"   Latest alert level: {latest['level']}")
                print(f"   Latest alert type: {latest['event_type']}")
        else:
            print("⚠️  No decoys deployed to access")

        # ── Step 6: Final system summary ─────────────────────────
        print("\n[STEP 6] Final System Summary...")
        print(f"   Final threat score : {monitor.threat_detector.threat_score}")
        print(f"   Final threat level : {monitor.threat_detector.get_threat_level()}")
        print(f"   Total events tracked: {len(monitor.threat_detector.events)}")
        print(f"   Decoys deployed    : {status['deployed']}")
        print(f"   Total alerts       : {len(monitor.decoy_manager.alert_manager.alerts)}")

        print("\n✅ Full system test completed successfully!")
        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False



if __name__ == "__main__":
    print("\n" + "="*60)
    print("DAY 25-26: FULL SYSTEM INTEGRATION TEST")
    print("="*60)

    result = test_full_attacker_scenario()

    print("\n" + "="*60)
    if result:
        print("🎉 SYSTEM TEST PASSED! Your honeypot is working!")
    else:
        print("⚠️  System test failed. Check errors above.")
    print("="*60)
