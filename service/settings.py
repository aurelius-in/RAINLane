from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    azure_openai_endpoint: str | None = Field(default=None, alias="AZURE_OPENAI_ENDPOINT")
    azure_openai_api_key: str | None = Field(default=None, alias="AZURE_OPENAI_API_KEY")
    anthropic_api_key: str | None = Field(default=None, alias="ANTHROPIC_API_KEY")

    # Optional storage
    aws_access_key_id: str | None = Field(default=None, alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str | None = Field(default=None, alias="AWS_SECRET_ACCESS_KEY")
    aws_region: str | None = Field(default=None, alias="AWS_REGION")
    s3_bucket: str | None = Field(default=None, alias="S3_BUCKET")

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = AppSettings()


