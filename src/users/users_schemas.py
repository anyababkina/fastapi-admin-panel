from fastapi import Form
from pydantic import BaseModel, SecretStr, EmailStr


class UserSchema(BaseModel):
    username: str = Form(max_length=20)
    password: SecretStr = Form(min_length=8)
    email: EmailStr

    @classmethod
    def as_form(cls, username: str = Form(max_length=20), email: EmailStr = Form(), password: SecretStr = Form(min_length=8)):
        return cls(username=username, email=email, password=password)
