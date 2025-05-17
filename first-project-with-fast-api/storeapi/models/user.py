from pydantic import BaseModel
from pydantic import ConfigDict

class User(BaseModel):
    id: int | None = None
    email: str

class UserIn(User):
    password: str