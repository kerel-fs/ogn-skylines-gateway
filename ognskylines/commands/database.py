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
def drop(sure='n'):
    """Drop all tables."""
    if sure == 'y':
        Base.metadata.drop_all(engine)
        print('Dropped all tables.')
    else:
        print("Add argument '--sure y' to drop all tables.")
