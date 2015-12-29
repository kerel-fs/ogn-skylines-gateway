from ognskylines.dbutils import session
from ognskylines.model import User, Device
from ognskylines.model.functions import insert_user, IntegrityError, NoResultFound
from ogn.utils import get_ddb, get_trackable


from manager import Manager
manager = Manager()


@manager.command
def insert(ogn_address, skylines_key, add_device='n'):
    """Insert a new user into the database."""
    try:
        insert_user(str(skylines_key), str(ogn_address), add_device == 'y')
    except ValueError as e:
        print('Invalid input, {}'.format(e))
        exit(-1)
    except NoResultFound as e:
        print('Device not in database (insert device to ddb.glidernet.org)')
        exit(-1)
    except IntegrityError:
        print('User already in the database.')

    user = User(ogn_address=ogn_address, skylines_key=int(skylines_key, 16))
    print('Added {}.'.format(user))


@manager.command
def import_ddb():
    """Import registered devices from the DDB (discards all devices before import)."""
    session.query(Device).delete()

    print("Import registered devices fom the DDB...")
    devices = get_trackable(get_ddb())
    for ogn_address in devices:
        device = Device(ogn_address=ogn_address[3:])
        session.add(device)
    session.commit()
    print("Imported {} devices.".format(len(devices)))
