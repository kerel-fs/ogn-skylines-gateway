from sqlalchemy.exc import IntegrityError

from ognskylines.dbutils import engine, session
from ognskylines.model import Base, User

from manager import Manager
database_manager = Manager()


@database_manager.command
def init():
    """Initialize the database."""
    Base.metadata.create_all(engine)
    print('Done.')


@database_manager.command
def insert(ogn_address, skylines_key):
    """Insert a new user into the database."""
    ogn_address = str(ogn_address)
    skylines_key = str(skylines_key)

    # Input validation
    failure = ''
    if not (len(ogn_address) == 6 and
            len(skylines_key) == 8):
        failure = 'Wrong input length.'
    try:
        int(skylines_key, 16)
        int(ogn_address, 16)
    except ValueError:
        failure = 'Address and Key must be hexadecimal.'

    if failure:
        print('Invalid input: {}'.format(failure))
    else:
        user = User(ogn_address=ogn_address, skylines_key=skylines_key)
        try:
            session.add(user)
            session.commit()
            print('Added user (ogn_address {}, skylines_key {}'.format(user.ogn_address, user.skylines_key))
        except IntegrityError:
            print('User already in the database.')
