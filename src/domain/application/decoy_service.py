# src/application/decoy_service.py
from ..interfaces.decoy_generator import IDecoyGenerator
from ..entities.decoy import Decoy
from typing import List

class DecoyService:
    """
    Orchestrates decoy operations based on threat levels
    Contains business logic for when and what decoys to deploy
    """
    
    def __init__(self, decoy_generator: IDecoyGenerator):
        """
        Initialize the decoy service
        
        Args:
            decoy_generator: Implementation of IDecoyGenerator interface
        """
        self.generator = decoy_generator
        self.deployed_decoys: List[Decoy] = []
    
    def generate_decoys_for_threat_level(self, threat_level: str, base_path: str) -> List[Decoy]:
        """
        Generate appropriate decoys based on threat level
        
        Args:
            threat_level: "Normal", "Elevated", "Suspicious", or "Critical"
            base_path: Base directory where decoys should be placed
            
        Returns:
            List of generated Decoy objects
        """
        decoys = []
        
        if threat_level == "Suspicious":
            # Deploy 2 decoys for suspicious activity
            decoys.append(self.generator.create_credential_decoy(f"{base_path}/passwords.txt"))
            decoys.append(self.generator.create_document_decoy(f"{base_path}/confidential_report.txt"))
            
        elif threat_level == "Critical":
            # Deploy 4 decoys for critical threats
            decoys.append(self.generator.create_credential_decoy(f"{base_path}/admin_passwords.txt"))
            decoys.append(self.generator.create_credential_decoy(f"{base_path}/api_keys.txt"))
            decoys.append(self.generator.create_config_decoy(f"{base_path}/database_config.yaml"))
            decoys.append(self.generator.create_document_decoy(f"{base_path}/financial_data.txt"))
        
        # Track deployed decoys
        self.deployed_decoys.extend(decoys)
        
        return decoys
    
    def is_decoy_file(self, file_path: str) -> bool:
        """
        Check if a file path is a deployed decoy

        Args:
            file_path: Path to check

        Returns:
            True if file is a decoy, False otherwise
        """
        # Normalize slashes for cross-platform comparison
        normalized = file_path.replace('\\', '/')
        return any(
            decoy.file_path.replace('\\', '/') == normalized
            for decoy in self.deployed_decoys
        )
    
    def get_deployed_decoys(self) -> List[Decoy]:
        """
        Get list of all deployed decoys
        
        Returns:
            List of Decoy objects
        """
        return self.deployed_decoys.copy()
