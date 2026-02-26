# Day 19-20: Decoy Tracking - Detailed Explanation

**Authors:** Aryan Jakkal & Dhirayshil Sarwade  
**Date Completed:** February 20, 2026  
**Topic:** Attack Tracking and Forensic Logging

---

## 🎯 What We Built

Today we enhanced the decoy system with detailed attack tracking. Now when an attacker accesses a decoy, the system captures comprehensive forensic information including timestamps, attack patterns, and behavior sequences.

---

## 📁 File Created: `src/monitor/attack_tracker.py`

### Purpose
Tracks and logs detailed information about every attack on decoy files for forensic analysis and security monitoring.

### Why We Need AttackTracker

**Problem:** DecoyManager detects when decoys are accessed, but doesn't keep detailed records.

**Solution:** AttackTracker maintains a complete history of all attacks with timestamps, patterns, and statistics.

---

## 🔍 Code Explanation

### Class Structure

```python
class AttackTracker:
    """
    Tracks detailed information about attacks on decoy files
    Records attacker behavior patterns and access sequences
    """
    
    def __init__(self):
        """Initialize the attack tracker"""
        self.logger = EventLogger()
        self.attacks = []  # List of all recorded attacks
        self.logger.log_info("AttackTracker initialized")
```

**State:**
- `self.attacks`: List storing all attack records
- `self.logger`: For logging attack events

---

### Method 1: record_attack()

```python
def record_attack(self, decoy_path: str, event_type: str, threat_level: str, 
                 threat_score: int, trigger_path: str = None):
```

**Purpose:** Records a single attack with all relevant details.

```python
    attack_info = {
        'timestamp': datetime.now().isoformat(),
        'decoy_path': decoy_path,
        'event_type': event_type,
        'threat_level': threat_level,
        'threat_score': threat_score,
        'trigger_path': trigger_path,
        'attack_id': len(self.attacks) + 1
    }
```

**Attack Information Captured:**
- `timestamp`: Exact time of attack (ISO format for parsing)
- `decoy_path`: Which decoy was accessed
- `event_type`: What action (created, modified, deleted)
- `threat_level`: Threat category at time of attack
- `threat_score`: Numeric threat score
- `trigger_path`: Original file that triggered deployment
- `attack_id`: Unique sequential ID

**Why ISO format?** `datetime.now().isoformat()` produces: `"2026-02-20T14:30:45.123456"` - easily parseable by other tools.

```python
    # Add to attacks list
    self.attacks.append(attack_info)
    
    # Log the attack
    self.logger.log_error(
        f"🚨 ATTACK #{attack_info['attack_id']} DETECTED | "
        f"Decoy: {decoy_path} | "
        f"Action: {event_type} | "
        f"Threat: {threat_level} ({threat_score}) | "
        f"Time: {attack_info['timestamp']}"
    )
```

**Dual logging:**
1. Store in memory (`self.attacks`)
2. Log to file (`logs/events.log`)

```python
    # Log to separate attack log file
    self._log_to_attack_file(attack_info)
    
    return attack_info
```

**Returns:** The attack info dictionary for immediate use.

---

### Method 2: _log_to_attack_file()

```python
def _log_to_attack_file(self, attack_info: Dict):
    """
    Write attack information to dedicated attack log file
    """
    import os
    
    # Create attacks directory if it doesn't exist
    if not os.path.exists('logs/attacks'):
        os.makedirs('logs/attacks')
```

**Safety:** Creates directory structure if needed.

```python
    # Write to attack log file
    attack_log_path = 'logs/attacks/attack_log.json'
    
    # Read existing attacks
    existing_attacks = []
    if os.path.exists(attack_log_path):
        try:
            with open(attack_log_path, 'r') as f:
                existing_attacks = json.load(f)
        except:
            existing_attacks = []
```

**Read-modify-write pattern:**
1. Read existing attacks from JSON file
2. Add new attack
3. Write everything back

**Why try-except?** Handles corrupted JSON files gracefully.

```python
    # Add new attack
    existing_attacks.append(attack_info)
    
    # Write back to file
    with open(attack_log_path, 'w') as f:
        json.dump(existing_attacks, f, indent=2)
```

**JSON format benefits:**
- Human-readable
- Machine-parseable
- Standard format for security tools
- Easy to import into analysis tools

---

### Method 3: get_attack_summary()

```python
def get_attack_summary(self) -> Dict:
    """
    Get summary of all recorded attacks
    
    Returns:
        Dictionary with attack statistics
    """
    if not self.attacks:
        return {
            'total_attacks': 0,
            'attacks': []
        }
```

**Edge case:** Returns empty summary if no attacks.

```python
    # Count attacks by type
    event_types = {}
    for attack in self.attacks:
        event_type = attack['event_type']
        event_types[event_type] = event_types.get(event_type, 0) + 1
```

**Dictionary counting pattern:**
- `event_types.get(event_type, 0)`: Get current count or 0
- `+ 1`: Increment count
- Result: `{'modified': 3, 'deleted': 1, 'created': 2}`

```python
    # Count attacks by threat level
    threat_levels = {}
    for attack in self.attacks:
        level = attack['threat_level']
        threat_levels[level] = threat_levels.get(level, 0) + 1
```

**Same pattern** for threat levels: `{'Suspicious': 2, 'Critical': 4}`

```python
    return {
        'total_attacks': len(self.attacks),
        'attacks': self.attacks,
        'by_event_type': event_types,
        'by_threat_level': threat_levels,
        'first_attack': self.attacks[0]['timestamp'] if self.attacks else None,
        'last_attack': self.attacks[-1]['timestamp'] if self.attacks else None
    }
```

**Complete summary includes:**
- Total count
- All attack records
- Breakdown by event type
- Breakdown by threat level
- First and last attack times

---

### Method 4: get_attack_pattern()

```python
def get_attack_pattern(self) -> List[str]:
    """
    Analyze attack pattern - sequence of actions
    
    Returns:
        List of event types in order
    """
    return [attack['event_type'] for attack in self.attacks]
```

**List comprehension:** Extracts just the event types in order.

**Example output:** `['modified', 'created', 'deleted', 'modified']`

**Why useful?** Reveals attacker behavior:
- `['modified', 'modified', 'modified']` = Reading files
- `['deleted', 'deleted', 'deleted']` = Destroying evidence
- `['created', 'modified', 'deleted']` = Testing then cleaning up

---

### Method 5: get_targeted_decoys()

```python
def get_targeted_decoys(self) -> List[str]:
    """
    Get list of decoys that were targeted
    
    Returns:
        List of unique decoy paths
    """
    return list(set([attack['decoy_path'] for attack in self.attacks]))
```

**Set operation:** Removes duplicates.

**Example:**
- Input: `['decoys/passwords.txt', 'decoys/api_keys.txt', 'decoys/passwords.txt']`
- Output: `['decoys/passwords.txt', 'decoys/api_keys.txt']`

**Why useful?** Shows which decoys are most attractive to attackers.

---

## 🔗 Integration with DecoyManager

### Updated DecoyManager.__init__()

```python
def __init__(self, decoy_base_path="decoys"):
    # ... existing code ...
    
    # Create attack tracker
    self.attack_tracker = AttackTracker()
    
    # Track the path that triggered deployment
    self.trigger_path = None
```

**New state:**
- `self.attack_tracker`: AttackTracker instance
- `self.trigger_path`: Remembers what triggered deployment

### Updated track_decoy_access()

```python
def track_decoy_access(self, file_path, event_type, threat_level, threat_score):
    # Check if this file is a deployed decoy
    if self.decoy_service.is_decoy_file(file_path):
        # Record the attack with detailed information
        attack_info = self.attack_tracker.record_attack(
            decoy_path=file_path,
            event_type=event_type,
            threat_level=threat_level,
            threat_score=threat_score,
            trigger_path=self.trigger_path
        )
        
        self.logger.log_error(
            f"🚨 ATTACKER CAUGHT! Decoy accessed: {file_path} | "
            f"Event: {event_type} | Threat: {threat_level} ({threat_score})"
        )
        return True
    
    return False
```

**Flow:**
1. Check if file is a decoy
2. If yes, record attack with AttackTracker
3. Log to main event log
4. Return True (attack detected)

### New Method: get_attack_statistics()

```python
def get_attack_statistics(self):
    """
    Get detailed attack statistics
    
    Returns:
        Dictionary with attack information
    """
    return self.attack_tracker.get_attack_summary()
```

**Convenience method:** Exposes AttackTracker statistics through DecoyManager.

---

## 🧪 Testing

### Test Flow

**Step 1: Initialize System**
```python
file_monitor = FileMonitor()
# Creates entire chain: FileMonitor → DecoyManager → AttackTracker
```

**Step 2: Trigger Deployment**
```python
# Access 5 sensitive files rapidly
for file_path in sensitive_files:
    file_monitor.on_created(MockEvent(file_path))
# Result: Threat score increases, decoys deployed
```

**Step 3: Simulate Attacks**
```python
# Attack 1: Modify decoy
file_monitor.on_modified(MockEvent(decoy_path))

# Attack 2: Read decoy
file_monitor.on_created(MockEvent(decoy_path))

# Attack 3: Delete decoy
file_monitor.on_deleted(MockEvent(decoy_path))

# Attack 4: Modify again
file_monitor.on_modified(MockEvent(decoy_path))
```

**Step 4: Analyze Statistics**
```python
stats = file_monitor.decoy_manager.get_attack_statistics()

print(f"Total Attacks: {stats['total_attacks']}")
print(f"By Type: {stats['by_event_type']}")
print(f"By Level: {stats['by_threat_level']}")
```

**Step 5: Analyze Patterns**
```python
pattern = attack_tracker.get_attack_pattern()
# Output: ['modified', 'created', 'deleted', 'modified']

targeted = attack_tracker.get_targeted_decoys()
# Output: ['decoys/passwords.txt', 'decoys/api_keys.txt']
```

---

## 📊 JSON Log File Format

### Example: `logs/attacks/attack_log.json`

```json
[
  {
    "timestamp": "2026-02-20T14:30:45.123456",
    "decoy_path": "decoys/passwords.txt",
    "event_type": "modified",
    "threat_level": "Suspicious",
    "threat_score": 65,
    "trigger_path": "test_tracking/secret_token.txt",
    "attack_id": 1
  },
  {
    "timestamp": "2026-02-20T14:30:46.234567",
    "decoy_path": "decoys/confidential_report.txt",
    "event_type": "created",
    "threat_level": "Suspicious",
    "threat_score": 70,
    "trigger_path": "test_tracking/secret_token.txt",
    "attack_id": 2
  }
]
```

**Benefits:**
- Structured data for analysis
- Timestamp for timeline reconstruction
- Trigger path shows attack origin
- Can be imported into SIEM tools

---

## 💡 Key Concepts Learned

### 1. Forensic Logging
Capturing detailed information for post-incident analysis:
- Who (attacker behavior)
- What (which decoys)
- When (timestamps)
- How (action sequence)

### 2. Data Structures for Analysis
- **Lists:** Ordered sequence of attacks
- **Dictionaries:** Structured attack information
- **Sets:** Unique values (targeted decoys)

### 3. JSON for Security Data
- Standard format
- Human-readable
- Machine-parseable
- Compatible with security tools

### 4. Pattern Analysis
Attack sequences reveal intent:
- Reconnaissance: Multiple reads
- Data theft: Modify/copy actions
- Cover-up: Delete actions

### 5. Statistics for Trends
Aggregated data shows:
- Most common attack types
- Most targeted decoys
- Attack frequency
- Threat level distribution

---

## 🔄 Complete Attack Flow

```
1. Attacker triggers suspicious activity
   ↓
2. ThreatDetector: Score reaches 51+
   ↓
3. DecoyManager: Deploys decoys, stores trigger_path
   ↓
4. Attacker discovers and accesses decoy
   ↓
5. FileMonitor: Detects decoy access
   ↓
6. DecoyManager.track_decoy_access(): Identifies as decoy
   ↓
7. AttackTracker.record_attack(): Captures details
   ↓
8. Logs to events.log (ERROR level)
   ↓
9. Logs to attack_log.json (structured data)
   ↓
10. Statistics updated in memory
   ↓
11. Available for analysis/alerting
```

---

## 🚀 What's Next (Day 21-22)

Now that we're tracking attacks, we need to:
1. **Create AlertManager** - Send alerts when attacks detected
2. **Multiple alert levels** - Low, Medium, High, Critical
3. **Alert formatting** - Clear, actionable alerts
4. **Alert logging** - Separate alert log file

---

## 📊 Project Status

**Completed:**
- ✅ File monitoring (Day 3-4)
- ✅ Event logging (Day 5-6)
- ✅ Threat detection (Day 9-10)
- ✅ System integration (Day 11-12)
- ✅ Decoy generation (Day 15-16)
- ✅ Decoy deployment (Day 17-18)
- ✅ Attack tracking (Day 19-20)

**Next:**
- ⏳ Alert system (Day 21-22)

**Progress:** 36% complete (20/56 days)

---

## 🎉 Congratulations!

You've built a **forensic-grade attack tracking system** that:
- ✅ Captures detailed attack information
- ✅ Logs to structured JSON files
- ✅ Analyzes attack patterns
- ✅ Generates statistics
- ✅ Identifies targeted decoys

**This is professional security monitoring!** 🛡️

---

**Next:** Day 21-22 - Alert System (real-time notifications)
