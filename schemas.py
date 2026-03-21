from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# USER SCHEMAS -----------------------------
class UserSchema(BaseModel):
    name: str
    email: str
    user_name: str
    password: str

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True

class ProfileEditSchema(BaseModel):
    name: str
    user_name: str

# END -----------------------------------------
        

#LETTERS SCHEMAS --------------------------------

class LetterCreate(BaseModel):
    user_name: str
    content: str
    status: Optional[str] = None

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

class MarkLetterAsRead(BaseModel):
    uuid: str
    is_read: bool