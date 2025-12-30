from models import User, db
from sqlalchemy.orm import sessionmaker

def get_session():
    Session = sessionmaker(bind=db)
    session = Session()
    return session