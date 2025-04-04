from typing import Optional

from pydantic import BaseModel, HttpUrl

class URLItem(BaseModel):
    target_url: HttpUrl
    custom_code: Optional[str]=None