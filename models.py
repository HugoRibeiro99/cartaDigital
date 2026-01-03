from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base

db = create_engine("sqlite:///database.db")

base = declarative_base()

class User(base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    email = Column("email", String, nullable=False)
    password = Column("password", String, nullable=False)
    user_id = Column("user_id", Boolean, default=False)
    
    def __init__(self, name, email, password):
        self.name = name
        self.email= email
        self.password = password
        




# base.metadata.create_all(db)