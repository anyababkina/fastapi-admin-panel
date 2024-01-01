from fastapi import Form
from pydantic import BaseModel


class ItemSchema(BaseModel):
    user_id: int
    name: str
    description: str

    @classmethod
    def as_form(cls, user_id: str = Form(), name: str = Form(), description: str = Form()):
        return cls(user_id=user_id, name=name, description=description)
