from pathlib import Path
from typing import Optional

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent


class RunConfig(BaseModel):
    host: str
    port: int


class ApiPrefix(BaseModel):
    domain: str = "/domain"
    history: str = "/history"
    file_search: str = "/file-search"
    domain_search: str = "/domain-search"


class DatabaseConfig(BaseModel):
    user: str
    password: str
    db_name: str
    port: int
    host: str
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    @property
    def url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


class BaseApiSettings(BaseModel):
    base_url: Optional[str] = None
    api_url: Optional[str] = None
    name: str
    table_id: str

    @property
    def page_url(self) -> str:
        return f"{self.base_url}-{self.name}/"

    @property
    def request_params(self) -> dict:
        return {
            "action": "get_wdtable",
            "table_id": self.table_id,
        }

    @property
    def default_post_data(self) -> dict:
        return {
            "draw": "1",
            "start": "0",
            "length": "25",
            "search[value]": "",
            "search[regex]": "false",
        }

    @property
    def default_headers(self) -> dict:
        return {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": self.page_url,
            "Origin": "https://sztfh.hu",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)",
        }


class WebsitesApiSettings(BaseApiSettings):
    name: str = "honlapok"
    table_id: str = "12"


class AdvertisingApiSettings(BaseApiSettings):
    name: str = "reklamoldalak"
    table_id: str = "35"


class RedisClient(BaseSettings):
    host: str
    port: int
    db: int = 0
    expires: int

    @property
    def celery_url_backend(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    base_url: str
    api_url: str

    website_api: WebsitesApiSettings = WebsitesApiSettings()
    advertising_api: AdvertisingApiSettings = AdvertisingApiSettings()
    redis: RedisClient
    run: RunConfig
    db: DatabaseConfig
    api_prefix: ApiPrefix = ApiPrefix()

    def __init__(self, **values):
        super().__init__(**values)
        for api in [self.website_api, self.advertising_api]:
            api.base_url = self.base_url
            api.api_url = self.api_url
            api.model_rebuild()


settings = Settings()
