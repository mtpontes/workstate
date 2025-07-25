class CredentialsValidationException(Exception):
    def __init__(self, errors: list[str]):
        self.errors = errors
        error_messages = "\n".join(f"- {error}" for error in errors)
        super().__init__(f"AWS credentials validation failed with {len(errors)} error(s):\n{error_messages}")
