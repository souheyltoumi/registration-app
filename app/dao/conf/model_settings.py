import os
import warnings

from pydantic import BaseSettings, BaseModel, PostgresDsn, AnyUrl, validator, Field
from typing import Dict
from functools import lru_cache

class WebService(BaseModel):
    nb_workers: int
    port: int
    frontend: str
    app_path: str
    profiling: bool
    reloading: bool

class Smtp(BaseModel):
    host: str
    port: int

class DataBase(BaseModel):
    dsn: PostgresDsn


class DbDict(Dict[str, DataBase]):
    def __getitem__(self, __key: str) -> DataBase:
        if __key not in self:
            raise JnError(
                f"Cannot find DB configuration DSN for '{__key}'", {"db_name": __key}
            )
        return super().__getitem__(__key)

class Settings(BaseSettings):
    env: str
    app: WebService
    smtp: Smtp
    db: Dict[str, DataBase] = {}

    class Config:
        case_sensitive = True
        env_nested_delimiter = "."
        env_file = ".env"

    @validator("db")
    def has_admn_db(cls, v):
        if "admin" not in v:
            raise ValueError("configuration : must provide admin db dsn")
        return DbDict(v)

@lru_cache()
def get_settings(**kwargs) -> Settings:
    encoded_conf = Settings(**kwargs)
    return encoded_conf
