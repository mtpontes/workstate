from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class StateDTO:
    """
    Data Transfer Object for S3 State metadata.
    Avoids direct dependency on Boto3 ObjectSummary in views and cache.
    """
    key: str
    size: int
    last_modified: datetime
    is_protected: bool = False
    
    @property
    def project(self) -> str:
        if "/" in self.key:
            return self.key.split("/")[0]
        return "[Legacy]"

    @property
    def filename(self) -> str:
        if "/" in self.key:
            return "/".join(self.key.split("/")[1:])
        return self.key
