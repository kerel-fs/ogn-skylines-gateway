import socket
import logging
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ogn.gateway.client import ognGateway
from ogn.model import AircraftBeacon

from skylines.utils import create_fix_message, fix_message_str

from ognskylines.model import User

logger = logging.getLogger(__name__)


class ognSkylinesGateway:
    def process_beacon(self, beacon):
        if type(beacon) is not AircraftBeacon:
            return
        logger.debug(fix_message_str(beacon))

        try:
            user = self.session.query(User).filter(User.ogn_address == beacon.address).one()
        except (MultipleResultsFound, NoResultFound):
            return
        skylines_key = user.skylines_key

        logger.info("TRACKED {} with key: {}".format(beacon.address, user.skylines_key_hex))
        message = create_fix_message(skylines_key,
                                     # NOTE: equivalent is (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).seconds * 1000
                                     (((beacon.timestamp.hour * 60) + beacon.timestamp.minute) * 60 + beacon.timestamp.second) * 1000,
                                     beacon.latitude,
                                     beacon.longitude,
                                     beacon.track,
                                     beacon.ground_speed / 3.6,
                                     0,
                                     int(beacon.altitude),
                                     beacon.climb_rate,
                                     0)
        self.socket.sendto(message, self.address)

    def __init__(self, session, aprs_user, host, port):
        self.session = session
        self.gateway = ognGateway(aprs_user)
        self.socket = socket.socket(socket.AF_INET,
                                    socket.SOCK_DGRAM)
        self.address = (host, port)

    def run(self):
        self.gateway.connect()
        self.gateway.run(callback=self.process_beacon, autoreconnect=True)

    def disconnect(self):
        self.gateway.disconnect()
