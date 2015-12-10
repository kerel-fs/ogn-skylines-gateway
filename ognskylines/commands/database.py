from ognskylines.dbutils import engine
from ognskylines.model import Base

from manager import Manager
manager = Manager()


@manager.command
def init():
    """Initialize the database."""
    Base.metadata.create_all(engine)
    print('Done.')


@manager.command
def drop(sure=0):
    """Drop all tables."""
    if sure:
        Base.metadata.drop_all(engine)
        print('Dropped all tables.')
    else:
