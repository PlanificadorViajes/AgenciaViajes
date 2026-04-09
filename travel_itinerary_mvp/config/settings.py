"""
Configuration settings for the travel itinerary MVP system.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any
import logging
import os

@dataclass
class SystemSettings:
    """System-wide configuration settings."""
    
    # Directories
    ROOT_DIR: Path = Path(__file__).parent.parent
    CONFIG_DIR: Path = ROOT_DIR / "config"
    PROMPTS_DIR: Path = CONFIG_DIR / "prompts"
    DATA_DIR: Path = ROOT_DIR / "data"
    LOGS_DIR: Path = ROOT_DIR / "logs"
    
    # Files
    ITINERARIES_FILE: Path = DATA_DIR / "itineraries.json"
    GENERATOR_PROMPT_FILE: Path = PROMPTS_DIR / "generator.txt"
    CRITIC_PROMPT_FILE: Path = PROMPTS_DIR / "critic.txt"
    
    # Agent Configuration
    MAX_ITERATIONS: int = 5
    MIN_QUALITY_SCORE: float = 7.0
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Model Configuration
    MODEL_NAME: str = "gpt-3.5-turbo"  # Placeholder for future LLM integration
    MODEL_TEMPERATURE: float = 0.7
    MODEL_MAX_TOKENS: int = 2000
    
    def __post_init__(self):
        """Ensure directories exist after initialization."""
        self.DATA_DIR.mkdir(exist_ok=True)
        self.LOGS_DIR.mkdir(exist_ok=True)

@dataclass
class QualityCriteria:
    """Quality criteria for plan evaluation."""
    
    CLARITY_WEIGHT: float = 0.15
    CONSISTENCY_WEIGHT: float = 0.20
    CONSTRAINT_COMPLIANCE_WEIGHT: float = 0.25
    OPTIMIZATION_WEIGHT: float = 0.20
    RISK_ASSESSMENT_WEIGHT: float = 0.10
    DETAIL_LEVEL_WEIGHT: float = 0.10
    
    def get_weights(self) -> Dict[str, float]:
        """Get all weights as a dictionary."""
        return {
            "clarity": self.CLARITY_WEIGHT,
            "consistency": self.CONSISTENCY_WEIGHT,
            "constraint_compliance": self.CONSTRAINT_COMPLIANCE_WEIGHT,
            "optimization": self.OPTIMIZATION_WEIGHT,
            "risk_assessment": self.RISK_ASSESSMENT_WEIGHT,
            "detail_level": self.DETAIL_LEVEL_WEIGHT
        }

def setup_logging(settings: SystemSettings) -> None:
    """Set up logging configuration."""
    log_file = settings.LOGS_DIR / "travel_itinerary.log"
    
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format=settings.LOG_FORMAT,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

# Global instances
SYSTEM_SETTINGS = SystemSettings()
QUALITY_CRITERIA = QualityCriteria()

# Initialize logging
setup_logging(SYSTEM_SETTINGS)
