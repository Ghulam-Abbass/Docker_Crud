from pydantic import BaseModel

class UserBase(BaseModel):
    title: str
    content: str
    amount: str
    check: bool

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass