from ognskylines.dbutils import session
from ognskylines.model import Device
from ogn.utils import get_ddb, get_trackable


from manager import Manager
manager = Manager()


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
