from typing import Optional

from pydantic import BaseSettings, Field


class BackupsConfig(BaseSettings):
    """
    Base App Configuration Parameters
    """
    django_secret: str = Field(..., env='APP_SECRET')
    django_host: Optional[str] = Field(..., env='APP_HOST')
    app_tz: Optional[str] = Field('UTC', env='APP_TZ')
    log_level: str = Field("WARNING", env='LOG_LEVEL')

    docker: bool = Field(True, env='DOCKER')
    db_name: str = Field('postgres', env='DB_NAME')
    db_host: str = Field('db', env='DB_HOST')
    db_user: str = Field('postgres', env='DB_USER')
    db_pass: Optional[str] = Field(None, env='DB_PASS')
    db_port: int = Field(5432, env='DB_PORT')
    redis_host: Optional[str] = Field(None, env='REDIS_HOST')
    debug: bool = Field(False, env='DEBUG')
    dev: bool = Field(False, env='DEV')
    db_backups_host: str = Field(..., env='DB_BACKUPS_HOST')
    mongo_db: str = Field(..., env='MONGO_CONNECTION_STRING')

    # Scaleway Configuration
    scaleway_region: str = Field('fr-par', env='SCALEWAY_REGION_NAME')
    scaleway_endpoint: str = Field('https://s3.fr-par.scw.cloud', env='SCALEWAY_ENDPOINT_URL')
    scaleway_bucket: str = Field(..., env='SCALEWAY_BUCKET_NAME')
    scaleway_key_id: str = Field(..., env='SCALEWAY_ACCESS_KEY_ID')
    scaleway_access_key: str = Field(..., env='SCALEWAY_SECRET_ACCESS_KEY')

    # oauth apps credentials
    google_app_key: Optional[str] = Field(..., env='GOOGLE_APP_KEY')
    google_app_secret: Optional[str] = Field(..., env='GOOGLE_APP_SECRET')
    github_app_key: Optional[str] = Field(..., env='GH_APP_KEY')
    github_app_secret: Optional[str] = Field(..., env='GH_APP_SECRET')
    todoist_app_key: Optional[str] = Field(..., env='TODOIST_KEY')
    todoist_app_secret: Optional[str] = Field(..., env='TODOIST_SECRET')
    dropbox_backups_token: Optional[str] = Field(..., env='DROPBOX_BACKUPS_TOKEN')
    slack_token: Optional[str] = Field(..., env="SLACK_API_TOKEN")

    # Personal access tokens
    up_time_key: Optional[str] = Field(..., env='UPTIME_KEY')
    mailgun_key: Optional[str] = Field(..., env='MAILGUN_KEY')
    sentry_dsn: Optional[str] = Field(..., env='SENTRY_DSN')

    @property
    def allowed_hosts(self) -> list:
        if not self.django_host:
            return []
        return self.django_host.split(',')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
