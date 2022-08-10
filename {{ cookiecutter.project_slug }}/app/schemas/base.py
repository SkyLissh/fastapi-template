from typing import Any

import orjson
from pydantic import BaseModel


def orjson_dumps(v: Any, *, default: Any) -> str:
    return orjson.dumps(v, default=default).decode("utf-8")


class Base(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dump = orjson_dumps
