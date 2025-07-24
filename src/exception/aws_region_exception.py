class RegionValidationError(ValueError):
    """Exception raised when an invalid AWS region is provided."""

    def __init__(self, region: str, valid_regions: list[str]):
        message = f"'{region}' is not a valid AWS region. Valid options are: {', '.join(valid_regions)}"
        super().__init__(message)
        self.region = region
        self.valid_regions = valid_regions
