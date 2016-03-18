from ognskylines.dbutils import session
from ognskylines.model import Device
import requests

from manager import Manager
manager = Manager()


DDB_URL = "http://ddb.glidernet.org/download/?j=1"


def get_ddb():
    devices = requests.get(DDB_URL).json()
    for device in devices['devices']:
        device.update({'identified': device['identified'] == 'Y',
                       'tracked': device['tracked'] == 'Y'})
        yield device


@manager.command
def import_ddb():
    """Import registered devices from the DDB (discards all devices before import)."""
    session.query(Device).delete()

    print("Import registered devices fom the DDB...")
    for device in get_ddb():
        if device['identified'] and device['tracked']:
            session.add(Device(ogn_address=device['device_id']))

    session.commit()
    print("Imported {} devices.".format(session.query(Device).count()))
