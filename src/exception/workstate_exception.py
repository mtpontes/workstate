class WorkstateException(Exception):
    """Base exception for all Workstate related errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
