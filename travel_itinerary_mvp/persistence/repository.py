"""
Repository for persisting travel itineraries.
"""
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..config.settings import SYSTEM_SETTINGS

logger = logging.getLogger(__name__)

class ItineraryRepository:
    """Repository for saving and loading travel itineraries."""
    
    def __init__(self):
        self.data_file = Path(SYSTEM_SETTINGS.DATA_DIR) / "itineraries.json"
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._ensure_data_file()
    
    def _ensure_data_file(self) -> None:
        """Ensure the data file exists."""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.data_file.exists():
            self._write_data([])
    
    def _read_data(self) -> List[Dict[str, Any]]:
        """Read data from JSON file."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.error(f"Error reading data file: {e}")
            return []
    
    def _write_data(self, data: List[Dict[str, Any]]) -> bool:
        """Write data to JSON file."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            return True
        except Exception as e:
            self.logger.error(f"Error writing data file: {e}")
            return False
    
    def save_itinerary(
        self, 
        itinerary: Dict[str, Any], 
        session_id: str,
        score: float,
        approved: bool,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Save an itinerary to the repository."""
        try:
            data = self._read_data()
            
            itinerary_record = {
                "id": session_id,
                "session_id": session_id,
                "created_at": datetime.now().isoformat(),
                "score": score,
                "approved": approved,
                "itinerary": itinerary,
                "metadata": metadata or {}
            }
            
            data.append(itinerary_record)
            self.logger.info(f"Saved new itinerary: {session_id}")
            
            return self._write_data(data)
            
        except Exception as e:
            self.logger.error(f"Error saving itinerary {session_id}: {e}")
            return False
    
    def get_itinerary(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve an itinerary by session ID."""
        try:
            data = self._read_data()
            for item in data:
                if item.get('session_id') == session_id:
                    return item
            return None
        except Exception as e:
            self.logger.error(f"Error retrieving itinerary {session_id}: {e}")
            return None
    
    def list_itineraries(self, limit: int = 10) -> List[Dict[str, Any]]:
        """List recent itineraries."""
        try:
            data = self._read_data()
            return sorted(data, key=lambda x: x.get('created_at', ''), reverse=True)[:limit]
        except Exception as e:
            self.logger.error(f"Error listing itineraries: {e}")
            return []
