from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserSchema(BaseModel):
    name: str
    email: str
    user_id: str
    password: str

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True

class LetterCreate(BaseModel):
    sender_id: int
    recipient_id: int
    content: str

class LetterResponse(BaseModel):
    id: int          
    sender_id: int   
    recipient_id: int
    content: str
    created_at: datetime
    status: str
    sent_at: Optional[datetime] = None
    delivery_at: Optional[datetime] = None

    class Config:
        from_attributes = True