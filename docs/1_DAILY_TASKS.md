# ✅ Daily Tasks & Checklists

**Authors:** Aryan Jakkal & Dhirayshil Sarwade  
**Project:** Adaptive File System Honeypot Agent

---

## 📌 HOW TO USE THIS FILE

**Simple 3-step process:**

1. **Check boxes ✅** as you complete each task
2. **Write what you learned** after each day
3. **Tell me when done:** "I completed Day X"

**Then I'll automatically update your progress tracker!** 🤖

---

## 📅 Day 1-2: Project Setup ✅ COMPLETED

**Date Completed:** February 8, 2026

**Tasks:**
- [x] Created virtual environment
- [x] Created project folders
- [x] Created pyproject.toml
- [x] Installed dependencies
- [x] Created main.py
- [x] Created config.yaml
- [x] Set up Git

**What I Learned:**
```
1. Virtual environments keep project dependencies isolated
2. pyproject.toml is the modern way to configure Python projects
3. Git workflow: status → add → commit → push
```

---

## 📅 Day 3-4: File Monitoring Basics ✅ COMPLETED

**Date Completed:** February 8, 2026

**Tasks:**
- [x] Learn watchdog library
- [x] Create FileMonitor class in `src/monitor/file_monitor.py`
- [x] Implement file change detection (created, modified, deleted)
- [x] Test monitoring on a test folder
- [x] Log events to console

**Code to Write:**
```python
# src/monitor/file_monitor.py
- FileMonitor class ✅
- on_created() method ✅
- on_modified() method ✅
- on_deleted() method ✅
```

**What I Learned:**
```
1. Watchdog library uses Observer pattern to monitor file system events in real-time
2. FileSystemEventHandler provides methods (on_created, on_modified, on_deleted) that run when files change
3. Observer.schedule() watches a directory continuously and calls event handlers automatically
4. Indentation is critical in Python - functions inside vs outside classes behave differently 

2. 

3. 
```

---

## 📅 Day 5-6: Event Logging ✅ COMPLETED

**Date Completed:** February 8, 2026

**Tasks:**
- [x] Create Logger class in `src/monitor/logger.py`
- [x] Log events to `logs/events.log` file
- [x] Add timestamps to logs
- [x] Add log levels (INFO, WARNING, ERROR)
- [x] Test logging system

**Code to Write:**
```python
# src/monitor/logger.py
- EventLogger class ✅
- log_info() method ✅
- log_warning() method ✅
- log_error() method ✅
- Format: [timestamp] [level] message ✅
```

**What I Learned:**
```
1. Python's logging module provides professional logging with timestamps and levels
2. Log levels (INFO, WARNING, ERROR) help categorize events by severity
3. Logging to files creates permanent records unlike print() statements
4. Relative imports (.logger) are used to import modules from the same package
5. Instance variables (self.logger) make objects available to all class methods
```
```
1. 

2. 

3. 
```

---

## 📅 Day 7-8: Testing & Bug Fixes ✅ COMPLETED

**Date Completed:** February 13, 2026

**Tasks:**
- [x] Write unit tests in `tests/simple_test.py`
- [x] Test logger creation and log levels
- [x] Test FileMonitor creation and event handling
- [x] Fix bugs (indentation, imports, typos)
- [x] All 4 tests passing successfully

**What I Learned:**
```
1. Testing is essential - write tests to verify code works correctly before moving forward
2. Try-except blocks catch errors gracefully without crashing the program
3. Mock objects let you test code without needing real files or events
4. Python's logging module has limitations - basicConfig() only works once per program
5. Indentation and function placement are critical in Python - functions must be defined before they're called
6. Tuple unpacking and generator expressions make code cleaner and more Pythonic
```

---

## 📅 Day 9-10: Threat Detection Algorithm ✅ COMPLETED

**Date Completed:** February 17, 2026

**Tasks:**
- [x] Create ThreatDetector class in `src/monitor/threat_detector.py`
- [x] Design scoring system (0-100 scale)
- [x] Implement basic rules:
  - Rapid file access = +20 points
  - Unusual time access = +15 points
  - Sensitive files = +25 points
  - Multiple deletions = +30 points
- [x] Test with sample data

**Code to Write:**
```python
# src/monitor/threat_detector.py
- ThreatDetector class ✅
- calculate_threat_score() method ✅
- Rules for suspicious behavior ✅
- check_rapid_access() method ✅
- check_unusual_time() method ✅
- check_sensitive_files() method ✅
- check_deletions() method ✅
- get_threat_level() method ✅
- get_threat_info() method ✅
```

**What I Learned:**
```
1. Threat detection uses scoring algorithms - multiple rules contribute points to calculate suspicion level
2. Time-based analysis is crucial - using timestamps (time.time()) to detect rapid access and unusual hours
3. List comprehensions filter data efficiently - [e for e in events if condition] creates filtered lists in one line
4. Dictionaries store event data - {'type': 'created', 'path': 'file.txt', 'time': timestamp} keeps related info together
5. Instance variables (self.variable) make data available to all methods in a class
6. Threshold-based decision making - different score ranges (0-30, 31-50, 51-70, 71-100) trigger different threat levels
7. The min() function caps values - min(score, 100) ensures score never exceeds 100 
```

---

## 📅 Day 11-12: System Integration (FileMonitor + ThreatDetector) ✅ COMPLETED

**Date Completed:** February 17, 2026

**Tasks:**
- [x] Integrate ThreatDetector with FileMonitor
- [x] Add threat detection to all event handlers (on_created, on_modified, on_deleted)
- [x] Log warnings when threat score >= 31
- [x] Test integrated system with real file operations
- [x] Fix pyproject.toml configuration issues
- [x] Install dependencies and run system successfully

**Code Changes:**
```python
# src/monitor/file_monitor.py
- Added import: from .threat_detector import ThreatDetector ✅
- Created instance: self.threat_detector = ThreatDetector() ✅
- Updated on_created() to send events and check threat level ✅
- Updated on_modified() to send events and check threat level ✅
- Updated on_deleted() to send events and check threat level ✅
```

**What I Learned:**
```
1. System integration connects multiple components - FileMonitor now uses ThreatDetector in real-time
2. Instance variables (self.threat_detector) make objects available across all class methods
3. Real-time threat detection works by: detect event → add to detector → calculate score → log if suspicious
4. pyproject.toml must have valid TOML syntax - corrupted config files prevent dependency installation
5. Testing integrated systems requires running the actual program, not just unit tests
6. The -e flag in pip install makes code changes take effect immediately without reinstalling
7. Step-by-step implementation helps understand how components connect and work together
```

---

## 📅 Day 13-14: Week 2 Review ✅ COMPLETED

**Date Completed:** February 17, 2026

**Tasks:**
- [x] Review all code from Week 1-2
- [x] Fix minor typos in docstrings
- [x] Test entire system with test_system.py
- [x] Update all documentation
- [x] Create Week 1-2 review document
- [x] Prepare for Week 3 (Decoy system)

**What I Learned:**
```
1. Code review is essential - catching typos and improving code quality before moving forward
2. System testing verifies all components work together, not just individually
3. Documentation review helps identify gaps and ensures everything is well-explained
4. Taking time to review prevents bugs and technical debt from accumulating
5. A solid foundation (Week 1-2) makes building advanced features (Week 3+) much easier
6. Regular reviews help consolidate learning and identify what you truly understand
7. Preparing for the next phase helps you start strong with clear goals
```

---

## 📅 Day 15-16: Decoy File Generator (Clean Architecture) ✅ COMPLETED

**Date Completed:** February 20, 2026

**IMPORTANT:** This day introduces Clean Architecture principles for future UI integration!

**Tasks:**
- [x] Create domain entity: `src/domain/entities/decoy.py` (Decoy class)
- [x] Create interface: `src/domain/interfaces/decoy_generator.py` (IDecoyGenerator)
- [x] Create use case: `src/domain/application/decoy_service.py` (DecoyService class)
- [x] Create implementation: `src/domain/infrastructure/file_decoy_generator.py` (FileDecoyGenerator)
- [x] Test decoy generation with clean architecture
- [x] All tests passing - decoys generated successfully

**Clean Architecture Structure:**
```
Domain Layer (Core Business Logic):
├── src/domain/entities/decoy.py - What is a decoy? ✅
└── src/domain/interfaces/decoy_generator.py - How should decoys be generated? ✅

Application Layer (Use Cases):
└── src/domain/application/decoy_service.py - Orchestrates decoy operations ✅

Infrastructure Layer (External Dependencies):
└── src/domain/infrastructure/file_decoy_generator.py - Actually creates files using Faker ✅
```

**Code to Write (Step by Step):**
```python
# Step 1: src/domain/entities/decoy.py ✅
- Decoy dataclass (type, path, content, created_time)

# Step 2: src/domain/interfaces/decoy_generator.py ✅
- IDecoyGenerator interface (abstract methods)

# Step 3: src/domain/application/decoy_service.py ✅
- DecoyService class (business logic orchestration)

# Step 4: src/domain/infrastructure/file_decoy_generator.py ✅
- FileDecoyGenerator class (implements IDecoyGenerator using Faker)
```

**What I Learned:**
```
1. Clean Architecture separates business logic from technical implementation - Domain, Application, Infrastructure layers
2. Domain layer has NO external dependencies - just pure Python classes and interfaces
3. Interfaces (IDecoyGenerator) define contracts - any implementation must have these methods
4. Application layer (DecoyService) orchestrates business logic - decides when/what decoys to deploy
5. Infrastructure layer (FileDecoyGenerator) uses external libraries like Faker to generate realistic content
6. Dependency injection makes testing easy - pass interface to DecoyService, not concrete implementation
7. Faker library generates realistic fake data - usernames, passwords, emails, addresses, documents
8. Clean architecture makes future UI integration easy - UI will only connect to Application layer
```

---

## 📅 Day 17-18: Decoy Deployment ✅ COMPLETED

**Date Completed:** February 20, 2026

**Tasks:**
- [x] Create DecoyManager class in `src/monitor/decoy_manager.py`
- [x] Integrate DecoyManager with FileMonitor
- [x] Deploy decoys automatically when threat score >= 51
- [x] Track deployed decoys
- [x] Detect when attacker accesses decoys
- [x] Test deployment logic - all working!

**What I Learned:**
```
1. System integration connects multiple layers - Monitor → DecoyManager → DecoyService → FileDecoyGenerator
2. DecoyManager bridges monitoring system with clean architecture decoy system
3. Automatic deployment triggers when threat score >= 51 (Suspicious or Critical)
4. Duplicate deployment prevention - only deploy once per session
5. Decoy access detection - can identify when attacker touches a decoy file
6. Real-time threat response - system adapts automatically to threats
7. Integration testing validates all components work together seamlessly
8. File system operations - creating directories, checking file existence
```

3. Deployment deduplication prevents repeatedly generating identical decoys for the same location/threat level.
```

---

## 📅 Day 19-20: Decoy Tracking ✅ COMPLETED

**Date Completed:** February 20, 2026

**Tasks:**
- [x] Create AttackTracker class in `src/monitor/attack_tracker.py`
- [x] Record detailed attack information (timestamp, decoy, action, threat level)
- [x] Log attacks to JSON file (`logs/attacks/attack_log.json`)
- [x] Capture attacker behavior patterns
- [x] Generate attack statistics and summaries
- [x] Test tracking system - all working!

**What I Learned:**
```
1. Attack tracking captures detailed forensic information - timestamp, file, action, threat level
2. JSON files provide structured, parseable attack logs for analysis
3. Attack patterns reveal attacker behavior - sequence of actions shows intent
4. Statistics help identify attack trends - most targeted decoys, common actions
5. Separate attack log files keep critical security data organized
6. Dictionary data structures efficiently store complex attack information
7. List comprehensions analyze patterns - [attack['type'] for attack in attacks]
8. Set operations find unique values - list(set([paths])) removes duplicates
```

---

## 📅 Day 21-22: Alert System ✅ COMPLETED

**Date Completed:** March 1, 2026

**Tasks:**
- [x] Create AlertManager class in `src/alert/manager.py`
- [x] Send alerts when decoy accessed
- [x] Log alerts to file (logs/alerts.log)
- [x] Add alert levels (Low, Medium, High, Critical)
- [x] Test alert system - all 6 tests passing

**Code to Write:**
```python
# src/alert/manager.py
- AlertManager class ✅
- create_alert() method ✅
- alert_decoy_accessed() method ✅
- alert_high_threat() method ✅
- get_alerts() method ✅
- get_alert_count() method ✅
```

**What I Learned:**
```
1. Alert systems provide structured notifications - separate from event logs, focused on security incidents
2. Logging handlers and formatters give fine control - FileHandler for files, different formatters for different outputs
3. Type hints improve code quality - Optional[str] means parameter can be None, helps catch errors early
4. Convenience methods reduce code duplication - alert_decoy_accessed() wraps create_alert() with preset values
5. List comprehensions filter data efficiently - [a for a in alerts if a['level'] == level] creates filtered lists
6. Dynamic alert levels based on threat scores - 71+ = Critical, 51-70 = High, 31-50 = Medium
7. Separate loggers for different purposes - AlertManager logger separate from EventLogger, different files
```

---

## 📅 Day 23-24: Enhanced Alerts & Integration ✅ COMPLETED

**Date Completed:** March 1, 2026

**Tasks:**
- [x] Integrate AlertManager with DecoyManager
- [x] Automatic alerts when decoy accessed
- [x] Enhanced alert details with context
- [x] Test integration - 2 tests passing
- [x] Complete security response chain

**Code Changes:**
```python
# src/monitor/decoy_manager.py
- Added AlertManager import ✅
- Added self.alert_manager = AlertManager() in __init__ ✅
- Updated track_decoy_access() to send alerts ✅

# tests/test_alert_integration.py
- Test alert sent on decoy access ✅
- Test alert log file created ✅
```

**What I Learned:**
```
1. System integration connects independent components - DecoyManager and AlertManager work together but stay separate
2. Automatic alerting improves response time - no manual intervention needed when decoys are accessed
3. Multiple logging destinations serve different purposes - events.log for details, alerts.log for notifications
4. Integration testing validates end-to-end flow - ensures all components work together correctly
5. Separation of concerns makes code maintainable - each class has one responsibility
6. Instance variables enable component communication - self.alert_manager makes AlertManager available to all methods
7. The complete security chain is now functional - detect → analyze → deploy → track → alert!
```

---

## 📅 Day 25-26: Integration Testing ✅ COMPLETED

**Date Completed:** March 1, 2026

**Tasks:**
- [x] Create full system integration test
- [x] Simulate complete attacker scenario
- [x] Verify all components work together
- [x] Test normal files → sensitive files → decoy deployment → alert chain
- [x] Full system test passed successfully!

**Files Created:**
```
tests/test_full_system.py  ✅
```

**What I Learned:**
```
1. Integration testing validates the complete system - not just individual parts
2. MockEvent class simulates real watchdog events without touching real files
3. One import (FileMonitor) gives access to the entire system - good design!
4. The complete security chain works: detect → score → deploy → track → alert
5. Step-by-step test output makes debugging easy - can see exactly where issues occur
6. if __name__ == "__main__" pattern keeps test code organized and reusable
7. Real attacker simulation: normal files → sensitive files → decoy access → alert
```

---

## 📅 Day 27-28: Week 4 Review

**Date:** _________

**Tasks:**
- [ ] Review all code
- [ ] Fix bugs
- [ ] Update documentation
- [ ] Test system thoroughly
- [ ] Prepare for Week 5

**What I Learned:**
```
1. 

2. 

3. 
```

---

## 📅 Day 29-56: Remaining Days

**Continue adding your daily tasks here as you progress!**

Each day, add:
- Date
- Tasks to complete
- What you learned

---

## 🔄 END OF DAY ROUTINE

**Every day, do these 3 things:**

1. ✅ Check off completed tasks above
2. 📝 Write what you learned
3. 💾 Git commit (see file: `2_PROGRESS_TRACKER.md`)

---

**Keep going! You're doing great!** 🚀
