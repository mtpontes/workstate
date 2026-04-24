import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

class CacheService:
    """
    Service responsible for managing local cache of S3 metadata.
    Stored in ~/.workstate/cache/metadata.json
    """
    
    CACHE_DIR = Path.home() / ".workstate" / "cache"
    CACHE_FILE = CACHE_DIR / "metadata.json"
    DEFAULT_TTL = 3600  # 1 hour in seconds

    @classmethod
    def get_cached_states(cls, project_name: str) -> Optional[List[Dict[str, Any]]]:
        """
        Retrieves cached states for a given project if valid and not expired.
        """
        cache = cls._load_cache()
        project_cache = cache.get(project_name)
        
        if not project_cache:
            return None
            
        timestamp = project_cache.get("timestamp", 0)
        if time.time() - timestamp > cls.DEFAULT_TTL:
            return None
            
        return project_cache.get("states")

    @classmethod
    def save_states_to_cache(cls, project_name: str, states: List[Dict[str, Any]]) -> None:
        """
        Saves a list of state metadata to the local cache.
        """
        cache = cls._load_cache()
        cache[project_name] = {
            "timestamp": time.time(),
            "states": states
        }
        cls._save_cache(cache)

    @classmethod
    def invalidate_project_cache(cls, project_name: str) -> None:
        """
        Removes cache for a specific project.
        """
        cache = cls._load_cache()
        if project_name in cache:
            del cache[project_name]
            cls._save_cache(cache)

    @classmethod
    def _load_cache(cls) -> Dict[str, Any]:
        """Loads cache from file, returns empty dict if not exists or invalid."""
        if not cls.CACHE_FILE.exists():
            return {}
            
        try:
            with open(cls.CACHE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    @classmethod
    def _save_cache(cls, cache: Dict[str, Any]) -> None:
        """Saves cache dict to file, creating directories if needed."""
        cls.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        try:
            with open(cls.CACHE_FILE, "w") as f:
                json.dump(cache, f, indent=2)
        except Exception:
            pass # Silent failure for cache write
