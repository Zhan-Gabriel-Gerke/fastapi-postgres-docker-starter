from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

class UserVerification(BaseModel):
    password: str = Field(min_length=3)
    new_password: str = Field(min_length=3)

class UserVerificationPhone(BaseModel):
    password: str = Field(min_length=3)
    new_phone_number: str =  Field(min_length=3)