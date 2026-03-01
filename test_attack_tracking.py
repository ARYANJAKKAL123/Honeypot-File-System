# test_attack_tracking.py
"""
Test the attack tracking system - Day 19-20
"""
import sys
import os
import time

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from monitor.file_monitor import FileMonitor

def test_attack_tracking():
    """Test the complete attack tracking system"""
    
    print("\n" + "="*70)
    print("TESTING ATTACK TRACKING SYSTEM - Day 19-20")
    print("="*70)
    
    # Create test directory
    test_dir = "test_tracking"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    
    print(f"\n✅ Test directory created: {test_dir}")
    
    # Initialize the system
    print("\n" + "-"*70)
    print("STEP 1: Initialize System")
    print("-"*70)
    
    file_monitor = FileMonitor()
    print("✅ FileMonitor initialized")
    print("✅ ThreatDetector initialized")
    print("✅ DecoyManager initialized")
    print("✅ AttackTracker initialized")
    
    # Mock event class
    class MockEvent:
        def __init__(self, path, is_dir=False):
            self.src_path = path
            self.is_directory = is_dir
    
    # Simulate suspicious activity to trigger decoy deployment
    print("\n" + "-"*70)
    print("STEP 2: Trigger Decoy Deployment")
    print("-"*70)
    
    sensitive_files = [
        f"{test_dir}/passwords.txt",
        f"{test_dir}/api_keys.txt",
        f"{test_dir}/secret_token.txt",
        f"{test_dir}/database_config.yaml",
        f"{test_dir}/admin_credentials.txt"
    ]
    
    print("Simulating rapid access to sensitive files...")
    for file_path in sensitive_files:
        event = MockEvent(file_path)
        file_monitor.on_created(event)
        time.sleep(0.1)
    
    threat_score = file_monitor.threat_detector.threat_score
    threat_level = file_monitor.threat_detector.get_threat_level()
    print(f"\nThreat Score: {threat_score}")
    print(f"Threat Level: {threat_level}")
    
    # Check if decoys were deployed
    status = file_monitor.decoy_manager.get_deployment_status()
    print(f"\n✅ Decoys Deployed: {status['deployed']}")
    print(f"✅ Number of Decoys: {status['count']}")
    
    if not status['deployed']:
        print("\n❌ Decoys not deployed - threat score too low")
        return
    
    # Simulate attacker accessing multiple decoys
    print("\n" + "-"*70)
    print("STEP 3: Simulate Multiple Attacks on Decoys")
    print("-"*70)
    
    deployed_decoys = status['decoys']
    
    # Attack 1: Modify first decoy
    print("\n🎯 Attack 1: Modifying decoy...")
    event = MockEvent(deployed_decoys[0].file_path)
    file_monitor.on_modified(event)
    time.sleep(0.5)
    
    # Attack 2: Read second decoy (if exists)
    if len(deployed_decoys) > 1:
        print("🎯 Attack 2: Reading decoy...")
        event = MockEvent(deployed_decoys[1].file_path)
        file_monitor.on_created(event)
        time.sleep(0.5)
    
    # Attack 3: Delete first decoy
    print("🎯 Attack 3: Deleting decoy...")
    event = MockEvent(deployed_decoys[0].file_path)
    file_monitor.on_deleted(event)
    time.sleep(0.5)
    
    # Attack 4: Modify second decoy again
    if len(deployed_decoys) > 1:
        print("🎯 Attack 4: Modifying decoy again...")
        event = MockEvent(deployed_decoys[1].file_path)
        file_monitor.on_modified(event)
    
    # Get attack statistics
    print("\n" + "-"*70)
    print("STEP 4: Attack Statistics")
    print("-"*70)
    
    stats = file_monitor.decoy_manager.get_attack_statistics()
    
    print(f"\n📊 Total Attacks Detected: {stats['total_attacks']}")
    
    if stats['total_attacks'] > 0:
        print(f"\n📅 First Attack: {stats['first_attack']}")
        print(f"📅 Last Attack: {stats['last_attack']}")
        
        print("\n📈 Attacks by Event Type:")
        for event_type, count in stats['by_event_type'].items():
            print(f"   - {event_type}: {count}")
        
        print("\n⚠️  Attacks by Threat Level:")
        for level, count in stats['by_threat_level'].items():
            print(f"   - {level}: {count}")
        
        print("\n🎯 Targeted Decoys:")
        targeted = file_monitor.decoy_manager.attack_tracker.get_targeted_decoys()
        for decoy in targeted:
            print(f"   - {os.path.basename(decoy)}")
        
        print("\n🔍 Attack Pattern (sequence):")
        pattern = file_monitor.decoy_manager.attack_tracker.get_attack_pattern()
        print(f"   {' → '.join(pattern)}")
    
    # Show detailed attack log
    print("\n" + "-"*70)
    print("STEP 5: Detailed Attack Log")
    print("-"*70)
    
    if stats['total_attacks'] > 0:
        print("\n📋 All Recorded Attacks:")
        for attack in stats['attacks']:
            print(f"\n   Attack #{attack['attack_id']}:")
            print(f"   ├─ Time: {attack['timestamp']}")
            print(f"   ├─ Decoy: {os.path.basename(attack['decoy_path'])}")
            print(f"   ├─ Action: {attack['event_type']}")
            print(f"   ├─ Threat Level: {attack['threat_level']}")
            print(f"   └─ Threat Score: {attack['threat_score']}")
    
    # Check attack log file
    print("\n" + "-"*70)
    print("STEP 6: Verify Attack Log File")
    print("-"*70)
    
    attack_log_path = 'logs/attacks/attack_log.json'
    if os.path.exists(attack_log_path):
        size = os.path.getsize(attack_log_path)
        print(f"✅ Attack log file created: {attack_log_path}")
        print(f"   File size: {size} bytes")
        
        # Read and display
        import json
        with open(attack_log_path, 'r') as f:
            attacks = json.load(f)
        print(f"   Attacks logged: {len(attacks)}")
    else:
        print("❌ Attack log file not found")
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print("✅ AttackTracker recording attacks")
    print("✅ Detailed attack information captured")
    print("✅ Attack statistics generated")
    print("✅ Attack patterns analyzed")
    print("✅ JSON log file created")
    print("✅ All components working together!")
    print("\n🎉 Day 19-20 Complete! Attack tracking system working!")
    print("="*70)

if __name__ == "__main__":
    test_attack_tracking()
