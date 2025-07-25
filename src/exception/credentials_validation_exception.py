class CredentialsValidationException(Exception):
    def __init__(self, errors: dict[str, str]):
        self.errors = errors
        error_messages = "\n".join(f"- {error}" for _, error in errors.items())
        super().__init__(f"AWS credentials validation failed with {len(errors.keys())} error(s):\n{error_messages}")
