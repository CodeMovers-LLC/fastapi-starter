# import datetime
from pydantic import BaseModel

class User(BaseModel):
    id: int
    user_id: str
