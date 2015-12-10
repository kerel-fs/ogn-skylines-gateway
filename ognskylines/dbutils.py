from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql:///ognskylines')

Session = sessionmaker(bind=engine)
session = Session()
