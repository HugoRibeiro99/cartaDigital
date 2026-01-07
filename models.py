from sqlalchemy import create_engine, Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base
from enum import Enum
from datetime import datetime

db = create_engine("sqlite:///database.db")

base = declarative_base()

class User(base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    email = Column("email", String, nullable=False)
    password = Column("password", String, nullable=False)
    user_id = Column("user_id", String, nullable=False)
    
    def __init__(self, name, email, password, user_id):
        self.name = name
        self.email= email
        self.password = password
        self.user_id = user_id
        


class LetterStatus(Enum):
    DRAFT = "draft"       # Rascunho
    SENT = "sent"         # Enviada
    ARCHIVED = "archived" # Arquivada 

class Letter(base):
    __tablename__ = "letters"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    sender_id = Column("sender_id", ForeignKey("users.id"), nullable=False)
    recipient_id = Column("recipient_id", ForeignKey("users.id"), nullable = False)
    content = Column("content", Text, nullable=False)
    status = Column("status", String, default=LetterStatus.DRAFT, nullable=False)
    created_at = Column("created_at", DateTime,default=datetime.now, nullable=False)
    sent_at = Column("sent_at", DateTime,default=None, nullable=True)
    delivery_at = Column("delivery_at", DateTime ,default=None, nullable=True)
    is_read = Column(Boolean, default=False)


# base.metadata.create_all(db)