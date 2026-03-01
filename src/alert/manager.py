"""
Alert Manager 
Handles security alerts when threats are detected or decoys are accessed 
"""

import logging 
import os
from datetime import datetime
from typing import Dict, List, Optional


class AlertManager:
    """Manages security alerts"""

    def __init__(self, alert_log_file='logs/alerts.log'):
        """
        Initialize the alert manager

        Args:
            alert_log_file: Path to the alert log file
        """
        self.alert_log_file = alert_log_file
        self.alerts = []

        # Create logs directory if it doesn't exist 
        log_dir = os.path.dirname(alert_log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Configure alert logging 
        self.logger = logging.getLogger('AlertManager')
        self.logger.setLevel(logging.INFO)

        # Create file handler
        file_handler = logging.FileHandler(alert_log_file)
        file_handler.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)

        # Add handler to logger (avoid duplicates)
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)

        self.logger.info("AlertManager initialized")

        
    def create_alert(self, level: str, event_type: str, message: str, 
                    file_path: Optional[str] = None, 
                    threat_score: Optional[int] = None) -> Dict:
        """
        Create a structured alert
        
        Args:
            level: Alert level (Low, Medium, High, Critical)
            event_type: Type of event (decoy_accessed, high_threat, etc.)
            message: Human-readable alert message
            file_path: Optional file path related to alert
            threat_score: Optional threat score
            
        Returns:
            Dictionary containing alert data
        """
        alert = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'event_type': event_type,
            'message': message,
            'file_path': file_path,
            'threat_score': threat_score
        }
        
        # Store in memory
        self.alerts.append(alert)
        
        # Log to file
        log_message = f"[{level}] {event_type}: {message}"
        if file_path:
            log_message += f" | File: {file_path}"
        if threat_score is not None:
            log_message += f" | Score: {threat_score}"
        
        # Use appropriate log level
        if level == "Critical":
            self.logger.critical(log_message)
        elif level == "High":
            self.logger.error(log_message)
        elif level == "Medium":
            self.logger.warning(log_message)
        else:  # Low
            self.logger.info(log_message)
        
        return alert

    
    def alert_decoy_accessed(self, file_path: str, event_type: str, 
                            threat_level: str, threat_score: int) -> Dict:
        """
        Create alert when a decoy file is accessed
        
        Args:
            file_path: Path to the decoy file
            event_type: Type of access (created, modified, deleted)
            threat_level: Current threat level
            threat_score: Current threat score
            
        Returns:
            Alert dictionary
        """
        message = f"🚨 DECOY ACCESSED! Attacker caught accessing decoy file. Event: {event_type}"
        
        return self.create_alert(
            level="Critical",
            event_type="decoy_accessed",
            message=message,
            file_path=file_path,
            threat_score=threat_score
        )
    
    def alert_high_threat(self, threat_score: int, threat_level: str, 
                         trigger_file: Optional[str] = None) -> Dict:
        """
        Create alert when threat score is high
        
        Args:
            threat_score: Current threat score
            threat_level: Current threat level
            trigger_file: File that triggered the high threat
            
        Returns:
            Alert dictionary
        """
        message = f"High threat detected: {threat_level} level activity"
        
        # Determine alert level based on threat score
        if threat_score >= 71:
            alert_level = "Critical"
        elif threat_score >= 51:
            alert_level = "High"
        else:
            alert_level = "Medium"
        
        return self.create_alert(
            level=alert_level,
            event_type="high_threat",
            message=message,
            file_path=trigger_file,
            threat_score=threat_score
        )
    
    def get_alerts(self, level: Optional[str] = None, 
                   limit: Optional[int] = None) -> List[Dict]:
        """
        Get stored alerts, optionally filtered by level
        
        Args:
            level: Optional filter by alert level
            limit: Optional limit number of results
            
        Returns:
            List of alert dictionaries
        """
        alerts = self.alerts
        
        # Filter by level if specified
        if level:
            alerts = [a for a in alerts if a['level'] == level]
        
        # Limit results if specified
        if limit:
            alerts = alerts[-limit:]  # Get last N alerts
        
        return alerts
    
    def get_alert_count(self) -> Dict[str, int]:
        """
        Get count of alerts by level
        
        Returns:
            Dictionary with counts for each level
        """
        counts = {
            'Low': 0,
            'Medium': 0,
            'High': 0,
            'Critical': 0,
            'Total': len(self.alerts)
        }
        
        for alert in self.alerts:
            level = alert['level']
            if level in counts:
                counts[level] += 1
        
        return counts
