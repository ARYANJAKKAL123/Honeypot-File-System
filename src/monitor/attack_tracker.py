# src/monitor/attack_tracker.py
from datetime import datetime
from .logger import EventLogger
from typing import List, Dict
import json

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
    
    def record_attack(self, decoy_path: str, event_type: str, threat_level: str, 
                     threat_score: int, trigger_path: str = None):
        """
        Record a decoy access (attack) with detailed information
        
        Args:
            decoy_path: Path to the accessed decoy file
            event_type: Type of access (created, modified, deleted)
            threat_level: Current threat level
            threat_score: Current threat score
            trigger_path: Original file that triggered the threat (optional)
        """
        attack_info = {
            'timestamp': datetime.now().isoformat(),
            'decoy_path': decoy_path,
            'event_type': event_type,
            'threat_level': threat_level,
            'threat_score': threat_score,
            'trigger_path': trigger_path,
            'attack_id': len(self.attacks) + 1
        }
        
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
        
        # Log to separate attack log file
        self._log_to_attack_file(attack_info)
        
        return attack_info
    
    def _log_to_attack_file(self, attack_info: Dict):
        """
        Write attack information to dedicated attack log file
        
        Args:
            attack_info: Dictionary containing attack details
        """
        import os
        
        # Create attacks directory if it doesn't exist
        if not os.path.exists('logs/attacks'):
            os.makedirs('logs/attacks')
        
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
        
        # Add new attack
        existing_attacks.append(attack_info)
        
        # Write back to file
        with open(attack_log_path, 'w') as f:
            json.dump(existing_attacks, f, indent=2)
    
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
        
        # Count attacks by type
        event_types = {}
        for attack in self.attacks:
            event_type = attack['event_type']
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        # Count attacks by threat level
        threat_levels = {}
        for attack in self.attacks:
            level = attack['threat_level']
            threat_levels[level] = threat_levels.get(level, 0) + 1
        
        return {
            'total_attacks': len(self.attacks),
            'attacks': self.attacks,
            'by_event_type': event_types,
            'by_threat_level': threat_levels,
            'first_attack': self.attacks[0]['timestamp'] if self.attacks else None,
            'last_attack': self.attacks[-1]['timestamp'] if self.attacks else None
        }
    
    def get_attack_pattern(self) -> List[str]:
        """
        Analyze attack pattern - sequence of actions
        
        Returns:
            List of event types in order
        """
        return [attack['event_type'] for attack in self.attacks]
    
    def get_targeted_decoys(self) -> List[str]:
        """
        Get list of decoys that were targeted
        
        Returns:
            List of unique decoy paths
        """
        return list(set([attack['decoy_path'] for attack in self.attacks]))
    
    def clear_attacks(self):
        """Clear all recorded attacks (for testing)"""
        self.attacks = []
        self.logger.log_info("Attack history cleared")
