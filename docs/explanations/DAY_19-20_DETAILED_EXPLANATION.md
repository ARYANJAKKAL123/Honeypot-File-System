# 📖 Day 19-20 Complete Breakdown: Decoy Tracking

**Date:** February 21, 2026  
**What You Built:** Decoy access tracking system to detect when attackers touch decoy files  
**Files Modified:** `src/monitor/decoy_manager.py`  
**Files Created:** `tests/test_decoy_tracking.py`

---

## 🎯 Quick Overview

**What you built:** A tracking system that monitors when decoy files are accessed and logs detailed information about the attacker's actions.

**Why it matters:** 
- Tracking is the "alarm trigger" in your honeypot
- When attackers access decoys, you know they're malicious
- Captures context (what, when, how) for security analysis
- Provides evidence of intrusion attempts

**Real-world use:** Security systems like Canary tokens, honeypots, and intrusion detection systems all use decoy tracking to catch attackers in the act.

---

## 🧩 Part 1: Understanding Decoy Tracking

### What is Decoy Tracking?

**Simple definition:**
Monitoring when someone accesses your fake files and recording what they do.

**Real-world analogy:**
- Decoys = Bait in a trap
- Tracking = Motion sensor on the trap
- When triggered = You know someone took the bait!

### Why Track Decoys?

1. **Detect attackers** - Normal users don't access fake files
2. **Gather evidence** - Record what the attacker did
3. **Trigger alerts** - Notify security team immediately
4. **Analyze behavior** - Understand attacker patterns

### What Gets Tracked?

When a decoy is accessed, we record:
- **File path** - Which decoy was touched
- **Event type** - Created, modified, or deleted
- **Timestamp** - When it happened
- **Threat level** - Current threat assessment
- **Threat score** - Numerical risk score

---

## 🧩 Part 2: The track_decoy_access() Method

### Location: `src/monitor/decoy_manager.py`

### What you added:

```python
def track_decoy_access(self, file_path, event_type, threat_level, threat_score):
    """
    Check if accessed file is a decoy and log if attacker caught
    
    Args:
        file_path: Path of accessed file
        event_type: Type of access (created, modified, deleted)
        threat_level: Current threat level
        threat_score: Current threat score
    """
    # Check if this file is a deployed decoy
    if self.decoy_service.is_decoy_file(file_path):
        self.logger.log_error(
            f"🚨 ATTACKER CAUGHT! Decoy accessed: {file_path} | "
            f"Event: {event_type} | Threat: {threat_level} ({threat_score})"
        )
        return True
    
    return False
```

---

## 📖 DETAILED EXPLANATION - Every Line:

### Line 1: Method Definition
```python
def track_decoy_access(self, file_path, event_type, threat_level, threat_score):
```

**What is this?**
- A method in the DecoyManager class
- Called whenever a file event occurs
- Checks if the file is a decoy

**Parameters explained:**

**`self`**
- Reference to the DecoyManager object
- Gives access to instance variables

**`file_path`**
- The full path to the file that was accessed
- Example: `"decoys/admin_passwords.txt"`
- This is what we're checking

**`event_type`**
- What happened to the file
- Values: `"created"`, `"modified"`, or `"deleted"`
- Tells us what the attacker did

**`threat_level`**
- Current threat assessment
- Values: `"Low"`, `"Medium"`, `"Suspicious"`, `"Critical"`
- Context about how dangerous the situation is

**`threat_score`**
- Numerical score (0-100)
- More precise than threat level
- Used for detailed analysis

---

### Lines 2-9: Docstring
```python
"""
Check if accessed file is a decoy and log if attacker caught

Args:
    file_path: Path of accessed file
    event_type: Type of access (created, modified, deleted)
    threat_level: Current threat level
    threat_score: Current threat score
"""
```

**What is this?**
- Documentation string
- Explains what the method does
- Lists all parameters
- Good practice for every method!

---

### Line 11: Check if File is a Decoy
```python
if self.decoy_service.is_decoy_file(file_path):
```

**Breaking it down:**

**`self.decoy_service`**
- The DecoyService object
- Created in `__init__`
- Manages all decoy operations

**`.is_decoy_file(file_path)`**
- Method that checks if a file is a decoy
- Takes the file path as input
- Returns `True` if it's a decoy, `False` if not

**How does it work internally?**
```python
# Inside DecoyService
def is_decoy_file(self, file_path):
    # Check if file_path matches any deployed decoy
    for decoy in self.deployed_decoys:
        if decoy.file_path == file_path:
            return True
    return False
```

**Why this check?**
- Not every file is a decoy
- Only want to alert on decoy access
- Normal files shouldn't trigger alerts

---

### Lines 12-15: Log the Attack
```python
self.logger.log_error(
    f"🚨 ATTACKER CAUGHT! Decoy accessed: {file_path} | "
    f"Event: {event_type} | Threat: {threat_level} ({threat_score})"
)
```

**Why log_error()?**
- Decoy access is a serious security event
- ERROR level = high priority
- Will stand out in logs

**Understanding the message:**

**`f"🚨 ATTACKER CAUGHT!"`**
- f-string (formatted string)
- 🚨 emoji makes it visually obvious
- Clear, urgent message

**`Decoy accessed: {file_path}`**
- Shows which decoy was touched
- Example: `"Decoy accessed: decoys/admin_passwords.txt"`
- Tells you what the attacker was looking for

**`Event: {event_type}`**
- Shows what they did
- Example: `"Event: modified"`
- Tells you how they interacted with it

**`Threat: {threat_level} ({threat_score})`**
- Shows current threat assessment
- Example: `"Threat: Critical (85)"`
- Provides context about the situation

**Full example output:**
```
🚨 ATTACKER CAUGHT! Decoy accessed: decoys/admin_passwords.txt | Event: modified | Threat: Critical (85)
```

---

### Line 16: Return True
```python
return True
```

**What does this mean?**
- Returns `True` = "Yes, this was a decoy access"
- Caller knows an attack was detected
- Can trigger additional actions (like alerts)

**Why return a value?**
- Allows other code to react
- Example: FileMonitor can send an alert
- Flexible design

---

### Line 18: Return False
```python
return False
```

**What does this mean?**
- Returns `False` = "No, this was not a decoy"
- Just a normal file access
- No alert needed

**Why return False?**
- Explicit is better than implicit
- Caller knows nothing suspicious happened
- Clean, clear code

---

## 🧩 Part 3: How It Integrates with FileMonitor

### The Flow:

```
1. File event occurs (user creates/modifies/deletes file)
        ↓
2. FileMonitor detects it (on_created, on_modified, on_deleted)
        ↓
3. ThreatDetector analyzes it (calculates threat score)
        ↓
4. DecoyManager checks if it's a decoy (track_decoy_access)
        ↓
5. If decoy: Log "ATTACKER CAUGHT!" and return True
        ↓
6. Future: Trigger alert system (Day 21-22)
```

### Example Integration in FileMonitor:

```python
def on_modified(self, event):
    """Called when a file is modified"""
    if not event.is_directory:
        # Log the event
        self.logger.log_info(f"File Modified: {event.src_path}")
        
        # Add to threat detector
        self.threat_detector.add_event('modified', event.src_path)
        
        # Get threat info
        threat_info = self.threat_detector.get_threat_info()
        
        # Check if it's a decoy access
        if self.decoy_manager:
            is_decoy = self.decoy_manager.track_decoy_access(
                file_path=event.src_path,
                event_type='modified',
                threat_level=threat_info['level'],
                threat_score=threat_info['score']
            )
            
            if is_decoy:
                # Attacker caught! Future: Send alert
                pass
```

---

## 🧩 Part 4: Testing Decoy Tracking

### File: `tests/test_decoy_tracking.py`

### Test 1: Manager-Level Tracking

```python
def test_decoy_manager_tracks_decoy_access(tmp_path):
    manager = DecoyManager(base_decoy_dir=".decoys", threshold=51)
    trigger_file = tmp_path / "suspicious_passwords.txt"

    # Deploy decoys
    deployed = manager.deploy_for_threat(
        threat_score=75,
        threat_level="Critical",
        trigger_path=str(trigger_file),
    )
    assert len(deployed) == 4

    # Track access to a deployed decoy
    tracked = manager.track_decoy_access(
        file_path=deployed[0].file_path,
        event_type="modified",
        threat_level="Critical",
        threat_score=82,
    )

    # Verify tracking worked
    assert tracked is not None
    assert tracked["file_path"] == deployed[0].file_path
    assert tracked["event_type"] == "modified"
    assert tracked["threat_level"] == "Critical"
    assert tracked["threat_score"] == 82
    assert len(manager.get_decoy_access_events()) == 1
```

**What this tests:**
1. ✅ Decoys can be deployed
2. ✅ Tracking detects decoy access
3. ✅ Context is captured correctly
4. ✅ Access events are stored

---

### Test 2: FileMonitor Integration

```python
def test_file_monitor_logs_decoy_access_context(tmp_path):
    monitor = FileMonitor()
    monitor.decoy_manager = DecoyManager(base_decoy_dir=".decoys", threshold=51)

    # Deploy decoys
    trigger_file = tmp_path / "password_seed.txt"
    deployed = monitor.decoy_manager.deploy_for_threat(
        threat_score=60,
        threat_level="Suspicious",
        trigger_path=str(trigger_file),
    )
    assert len(deployed) == 2

    # Simulate attacker touching a decoy
    class MockEvent:
        def __init__(self, src_path: str):
            self.src_path = src_path
            self.is_directory = False

    monitor.on_modified(MockEvent(deployed[0].file_path))

    # Verify tracking in monitor
    events = monitor.decoy_manager.get_decoy_access_events()
    assert len(events) >= 1
    assert events[-1]["file_path"] == deployed[0].file_path
    assert events[-1]["event_type"] == "modified"
```

**What this tests:**
1. ✅ FileMonitor integrates with DecoyManager
2. ✅ File events trigger tracking
3. ✅ Mock events work correctly
4. ✅ End-to-end flow works

---

## 💡 Key Concepts You Learned

### 1. Decoy Tracking
**What:** Monitoring access to fake files
**Why:** Detect attackers who touch decoys
**How:** Check if accessed file is a decoy, log if yes

### 2. Context Capture
**What:** Recording details about the event
**Why:** Provides evidence and analysis data
**How:** Pass event_type, threat_level, threat_score

### 3. Integration Testing
**What:** Testing how components work together
**Why:** Ensures end-to-end functionality
**How:** Test FileMonitor + DecoyManager together

### 4. Return Values for Control Flow
**What:** Returning True/False to indicate results
**Why:** Allows caller to react appropriately
**How:** Return True if decoy, False if not

### 5. Logging Severity Levels
**What:** Using ERROR level for security events
**Why:** Makes critical events stand out
**How:** Use log_error() for decoy access

---

## 🔗 How This Fits in Your Honeypot Project

### Current State (Day 19-20):
✅ **Decoy tracking built** - Can detect when attackers access decoys

### The Complete Flow (Days 1-20):

```
File Event Occurs
    ↓
FileMonitor detects it (Day 3-4)
    ↓
EventLogger logs it (Day 5-6)
    ↓
ThreatDetector scores it (Day 9-10)
    ↓
If threat score >= 51:
    DecoyManager deploys decoys (Day 17-18)
    ↓
If decoy accessed:
    DecoyManager tracks it (Day 19-20) ✅ YOU ARE HERE
    ↓
Next: AlertManager sends alert (Day 21-22)
```

### Why This Matters:

**Security Response Chain:**
1. **Detect** - FileMonitor sees file activity
2. **Analyze** - ThreatDetector scores behavior
3. **Respond** - DecoyManager deploys traps
4. **Catch** - Tracking detects decoy access ✅
5. **Alert** - (Next: Day 21-22)

---

## 🎓 What You Should Understand Now

After reading this, you should be able to explain:

1. ✅ What decoy tracking is and why it's important
2. ✅ How track_decoy_access() works line by line
3. ✅ What information is captured when a decoy is accessed
4. ✅ How tracking integrates with FileMonitor
5. ✅ Why we use ERROR level logging for decoy access
6. ✅ How to test decoy tracking (manager and integration)
7. ✅ What return values mean (True = decoy, False = not)
8. ✅ How this fits into the complete honeypot system

---

## 🚀 Next Steps

1. **Review this document** - Make sure you understand everything

2. **Check the logs** - Look at `logs/events.log` to see tracking in action

3. **Ready for Day 21-22** - Alert System!
   - Will send notifications when decoys are accessed
   - Build on the tracking we just completed
   - Complete the security response chain

---

## 📊 Day 19-20 Summary

**What you accomplished:**
- ✅ Added `track_decoy_access()` method to DecoyManager
- ✅ Integrated tracking with FileMonitor
- ✅ Captured event context (type, threat level, score)
- ✅ Logged "ATTACKER CAUGHT!" messages
- ✅ Created comprehensive tests
- ✅ Verified end-to-end functionality

**Files modified:**
- `src/monitor/decoy_manager.py` - Added tracking method

**Files created:**
- `tests/test_decoy_tracking.py` - Tracking tests

**Lines of code:** ~50 lines (method + tests)

**Key achievement:** Your honeypot can now detect when attackers access decoys! 🎉

---

**Congratulations on completing Day 19-20!** 🎉

You've built a complete decoy tracking system that catches attackers in the act!

---

**Last Updated:** February 21, 2026
