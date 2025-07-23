from src.templates.code_tool import CodeTool

MISSING_AWS_BUCKET_NAME = "Missing required environment variable: 'WORKSTATE_S3_BUCKET_NAME'."
MISSING_AWS_CREDENTIALS_MSG = (
    "Missing required AWS credentials in environment variables: 'AWS_ACCESS_KEY_ID' and/or 'AWS_SECRET_ACCESS_KEY'."
)
VALID_CODE_TOOLS_OPTIONS = f"Tool to use ({CodeTool.get_valid_values()})"
