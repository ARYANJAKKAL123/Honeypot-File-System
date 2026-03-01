# src/monitor/decoy_manager.py
from domain.application.decoy_service import DecoyService
from domain.infrastructure.file_decoy_generator import FileDecoyGenerator
from .logger import EventLogger
from .attack_tracker import AttackTracker
import os

class DecoyManager:
    """
    Manages decoy deployment and tracking for the monitoring system
    Bridges FileMonitor with DecoyService (clean architecture)
    """
    
    def __init__(self, decoy_base_path="decoys"):
        """
        Initialize the decoy manager
        
        Args:
            decoy_base_path: Base directory for deploying decoys
        """
        # Create decoy generator (Infrastructure layer)
        generator = FileDecoyGenerator()
        
        # Create decoy service (Application layer)
        self.decoy_service = DecoyService(generator)
        
        # Create attack tracker
        self.attack_tracker = AttackTracker()
        
        # Set up decoy deployment path
        self.decoy_base_path = decoy_base_path
        
        # Create decoy directory if it doesn't exist
        if not os.path.exists(decoy_base_path):
            os.makedirs(decoy_base_path)
        
        # Initialize logger
        self.logger = EventLogger()
        self.logger.log_info(f"DecoyManager initialized - decoys will be deployed to: {decoy_base_path}")
        
        # Track if decoys have been deployed (prevent duplicate deployments)
        self.decoys_deployed = False
        
        # Track the path that triggered deployment
        self.trigger_path = None
    
    def deploy_for_threat(self, threat_score, threat_level, trigger_path):
        """
        Deploy decoys based on threat level
        
        Args:
            threat_score: Current threat score (0-100)
            threat_level: Threat level category
            trigger_path: File path that triggered the threat
            
        Returns:
            List of deployed Decoy objects, or None if no deployment
        """
        # Only deploy for Suspicious (51-70) or Critical (71-100)
        if threat_score < 51:
            return None
        
        # Prevent duplicate deployments
        if self.decoys_deployed:
            return None
        
        # Store trigger path for attack tracking
        self.trigger_path = trigger_path
        
        # Deploy decoys using DecoyService
        self.logger.log_warning(
            f"Deploying decoys for {threat_level} threat (Score: {threat_score}) "
            f"triggered by: {trigger_path}"
        )
        
        decoys = self.decoy_service.generate_decoys_for_threat_level(
            threat_level, 
            self.decoy_base_path
        )
        
        # Mark as deployed
        self.decoys_deployed = True
        
        # Log deployment details
        self.logger.log_warning(
            f"✅ Deployed {len(decoys)} decoy(s): " +
            ", ".join([os.path.basename(d.file_path) for d in decoys])
        )
        
        return decoys
    
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
    
    def get_deployment_status(self):
        """
        Get current decoy deployment status
        
        Returns:
            Dictionary with deployment information
        """
        deployed_decoys = self.decoy_service.get_deployed_decoys()
        
        return {
            'deployed': self.decoys_deployed,
            'count': len(deployed_decoys),
            'decoys': deployed_decoys,
            'base_path': self.decoy_base_path
        }
    
    def get_attack_statistics(self):
        """
        Get detailed attack statistics
        
        Returns:
            Dictionary with attack information
        """
        return self.attack_tracker.get_attack_summary()
