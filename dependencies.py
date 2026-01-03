from models import User, db
from sqlalchemy.orm import sessionmaker

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()