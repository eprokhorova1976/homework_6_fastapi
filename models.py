from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, validator


class UserCreate(BaseModel):
    username: str = Field(..., max_length=80)
    surname: str = Field(..., max_length=120)
    email: EmailStr = Field(..., max_length=80)
    password: str = Field(max_length=120)


class UserOut(BaseModel):
    id: int
    username: str
    surname: str
    email: EmailStr

    class Config:
        from_attributes = True


class ExcursionCreate(BaseModel):
    title: str
    description: str
    price: float


class ExcursionOut(BaseModel):
    id: int
    title: str
    description: str
    price: float

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    user_id: int
    product_id: int


class OrderOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    order_date: datetime
    status: str

    class Config:
        from_attributes = True