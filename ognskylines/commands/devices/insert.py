from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ognskylines.dbutils import session
from ognskylines.model import User, Device

from ogn.utils import get_ddb, get_trackable

from manager import Manager
manager = Manager()


@manager.command
def insert(ogn_address, skylines_key, add_device='n'):
    """Insert a new user into the database."""
    ogn_address = str(ogn_address)
    skylines_key = str(skylines_key)

    # Input validation
    failure = ''
    if not (len(ogn_address) == 6 and
            len(skylines_key) == 8):
        failure = 'Wrong input length.'
    try:
        _skylines_key = int(skylines_key, 16)
        int(ogn_address, 16)
    except ValueError:
        failure = 'Address and Key must be hexadecimal.'
    try:
        session.query(Device).filter(Device.ogn_address == ogn_address).one()
    except (MultipleResultsFound, NoResultFound):
        if not add_device == 'y':
            failure = 'Device not registered in the ddb.'
        else:
            device = Device(ogn_address=ogn_address)
            session.add(device)

    if failure:
        print('Invalid input: {}'.format(failure))
    else:
        user = User(ogn_address=ogn_address, skylines_key=_skylines_key)
        try:
            session.add(user)
            session.commit()
            print('Added {}.'.format(user))
        except IntegrityError:
            print('User already in the database.')


@manager.command
def import_ddb():
    """Import registered devices from the DDB (flushed the device list)."""
    session.query(Device).delete()

    print("Import registered devices fom the DDB...")
    devices = get_trackable(get_ddb())
    for ogn_address in devices:
        device = Device(ogn_address=ogn_address[3:])
        session.add(device)
    session.commit()
    print("Imported {} devices.".format(len(devices)))
