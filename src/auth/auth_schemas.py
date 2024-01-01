from fastapi import Form
from pydantic import BaseModel, Field, EmailStr, SecretStr


class AdminRegistration(BaseModel):
    username: str = Field(max_length=20)
    email: EmailStr
    password: SecretStr = Field(min_length=8)

    @classmethod
    def as_form(cls, username: str = Form(max_length=20), email: EmailStr = Form(), password: SecretStr = Form(min_length=8)):
        return cls(username=username, email=email, password=password)


class AdminLogin(BaseModel):
    email: EmailStr
    password: SecretStr = Field(min_length=8)

    @classmethod
    def as_form(cls, email: EmailStr = Form(), password: SecretStr = Form(min_length=8)):
        return cls(email=email, password=password)