"""
Tests for AlertManager
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.alert.manager import AlertManager
import time


def test_alert_manager_creation():
    """Test that AlertManager can be created"""
    print("\n" + "="*60)
    print("TEST 1: AlertManager Creation")
    print("="*60)
    
    try:
        manager = AlertManager('logs/test_alerts.log')
        print("✅ AlertManager created successfully")
        print(f"   Alert log file: {manager.alert_log_file}")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def test_create_alert():
    """Test creating a basic alert"""
    print("\n" + "="*60)
    print("TEST 2: Create Basic Alert")
    print("="*60)
    
    try:
        manager = AlertManager('logs/test_alerts.log')
        
        # Create a test alert
        alert = manager.create_alert(
            level="High",
            event_type="test_event",
            message="This is a test alert",
            file_path="test_file.txt",
            threat_score=75
        )
        
        print("✅ Alert created successfully")
        print(f"   Level: {alert['level']}")
        print(f"   Event Type: {alert['event_type']}")
        print(f"   Message: {alert['message']}")
        print(f"   File: {alert['file_path']}")
        print(f"   Score: {alert['threat_score']}")
        print(f"   Timestamp: {alert['timestamp']}")
        
        # Check if alert was stored
        if len(manager.alerts) == 1:
            print("✅ Alert stored in memory")
        else:
            print("❌ Alert not stored properly")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def test_decoy_accessed_alert():
    """Test decoy accessed alert"""
    print("\n" + "="*60)
    print("TEST 3: Decoy Accessed Alert")
    print("="*60)
    
    try:
        manager = AlertManager('logs/test_alerts.log')
        
        # Create decoy accessed alert
        alert = manager.alert_decoy_accessed(
            file_path="decoys/admin_passwords.txt",
            event_type="modified",
            threat_level="Critical",
            threat_score=95
        )
        
        print("✅ Decoy accessed alert created")
        print(f"   Level: {alert['level']}")
        print(f"   Message: {alert['message']}")
        print(f"   File: {alert['file_path']}")
        print(f"   Score: {alert['threat_score']}")
        
        # Verify it's Critical level
        if alert['level'] == "Critical":
            print("✅ Correct alert level (Critical)")
        else:
            print(f"❌ Wrong alert level: {alert['level']}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def test_high_threat_alert():
    """Test high threat alert"""
    print("\n" + "="*60)
    print("TEST 4: High Threat Alert")
    print("="*60)
    
    try:
        manager = AlertManager('logs/test_alerts.log')
        
        # Test different threat scores
        test_cases = [
            (85, "Critical"),  # Score 85 should be Critical
            (65, "High"),      # Score 65 should be High
            (45, "Medium"),    # Score 45 should be Medium
        ]
        
        for score, expected_level in test_cases:
            alert = manager.alert_high_threat(
                threat_score=score,
                threat_level="Test",
                trigger_file="test.txt"
            )
            
            if alert['level'] == expected_level:
                print(f"✅ Score {score} → {expected_level} level (correct)")
            else:
                print(f"❌ Score {score} → {alert['level']} (expected {expected_level})")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def test_get_alerts():
    """Test getting and filtering alerts"""
    print("\n" + "="*60)
    print("TEST 5: Get and Filter Alerts")
    print("="*60)
    
    try:
        manager = AlertManager('logs/test_alerts.log')
        
        # Create multiple alerts
        manager.create_alert("Critical", "test1", "Critical alert 1")
        manager.create_alert("High", "test2", "High alert 1")
        manager.create_alert("Critical", "test3", "Critical alert 2")
        manager.create_alert("Medium", "test4", "Medium alert 1")
        
        # Get all alerts
        all_alerts = manager.get_alerts()
        print(f"✅ Total alerts: {len(all_alerts)}")
        
        # Get only Critical alerts
        critical_alerts = manager.get_alerts(level="Critical")
        print(f"✅ Critical alerts: {len(critical_alerts)}")
        
        if len(critical_alerts) == 2:
            print("✅ Filter by level works correctly")
        else:
            print(f"❌ Expected 2 Critical alerts, got {len(critical_alerts)}")
            return False
        
        # Get last 2 alerts
        last_two = manager.get_alerts(limit=2)
        print(f"✅ Last 2 alerts: {len(last_two)}")
        
        if len(last_two) == 2:
            print("✅ Limit works correctly")
        else:
            print(f"❌ Expected 2 alerts, got {len(last_two)}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def test_alert_count():
    """Test alert counting"""
    print("\n" + "="*60)
    print("TEST 6: Alert Count")
    print("="*60)
    
    try:
        manager = AlertManager('logs/test_alerts.log')
        
        # Create alerts of different levels
        manager.create_alert("Critical", "test", "Critical 1")
        manager.create_alert("Critical", "test", "Critical 2")
        manager.create_alert("High", "test", "High 1")
        manager.create_alert("Medium", "test", "Medium 1")
        manager.create_alert("Low", "test", "Low 1")
        
        # Get counts
        counts = manager.get_alert_count()
        
        print("✅ Alert counts:")
        print(f"   Critical: {counts['Critical']}")
        print(f"   High: {counts['High']}")
        print(f"   Medium: {counts['Medium']}")
        print(f"   Low: {counts['Low']}")
        print(f"   Total: {counts['Total']}")
        
        # Verify counts
        if counts['Critical'] == 2 and counts['High'] == 1 and counts['Total'] == 5:
            print("✅ Counts are correct")
            return True
        else:
            print("❌ Counts are incorrect")
            return False
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def run_all_tests():
    """Run all tests and show summary"""
    print("\n" + "="*60)
    print("RUNNING ALL ALERT MANAGER TESTS")
    print("="*60)
    
    tests = [
        ("AlertManager Creation", test_alert_manager_creation),
        ("Create Basic Alert", test_create_alert),
        ("Decoy Accessed Alert", test_decoy_accessed_alert),
        ("High Threat Alert", test_high_threat_alert),
        ("Get and Filter Alerts", test_get_alerts),
        ("Alert Count", test_alert_count),
    ]
    
    results = []
    for name, test_func in tests:
        result = test_func()
        results.append((name, result))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print("\n" + "-"*60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! AlertManager is working perfectly!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review the errors above.")
    
    print("="*60)


if __name__ == "__main__":
    run_all_tests()
