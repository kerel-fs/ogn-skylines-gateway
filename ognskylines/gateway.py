import socket
import logging

from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ogn.client import AprsClient
from ogn.parser import parse_aprs, parse_ogn_beacon, ParseError

from skylines.utils import create_fix_message, fix_message_str

from ognskylines.model import User, Device

logger = logging.getLogger(__name__)


class ognSkylinesGateway:
    def forward_aircraft_beacon(self, beacon):
        try:
            user = self.session.query(User).filter(User.ogn_address == beacon['address']).one()
        except (MultipleResultsFound, NoResultFound):
            return
        skylines_key = user.skylines_key

        logger.info("TRACKED {} with key: {}".format(beacon['address'], user.skylines_key_hex))
        logger.debug(fix_message_str(beacon))
        message = create_fix_message(skylines_key,
                                     # NOTE: equivalent is (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).seconds * 1000
                                     (((beacon['timestamp'].hour * 60) + beacon['timestamp'].minute) * 60 + beacon['timestamp'].second) * 1000,
                                     beacon['latitude'],
                                     beacon['longitude'],
                                     beacon['track'],
                                     beacon['ground_speed'] / 3.6,
                                     0,
                                     int(beacon['altitude']),
                                     beacon['climb_rate'],
                                     0)
        self.socket.sendto(message, self.address)

    def update_devices_list(self, beacon):
        try:
            device = self.session.query(Device).filter(Device.ogn_address == beacon['address']).one()
        except (MultipleResultsFound, NoResultFound):
            return

        device.timestamp = beacon['timestamp']
        device.set_location(longitude=beacon['longitude'], latitude=beacon['latitude'])

        self.session.commit()
        logger.debug(" {} SEEN AT {}".format(device.ogn_address, device.timestamp))

    def process_beacon(self, raw_message):
        if raw_message[0] == '#':
            return

        try:
            beacon = parse_aprs(raw_message)
            beacon.update(parse_ogn_beacon(beacon['comment']))
        except ParseError as e:
            logger.error(e.message)
            return

        if beacon['beacon_type'] == 'aircraft_beacon':
            self.forward_aircraft_beacon(beacon)
            self.update_devices_list(beacon)

    def __init__(self, session, aprs_user, host, port):
        self.session = session
        self.client = AprsClient(aprs_user)
        self.socket = socket.socket(socket.AF_INET,
                                    socket.SOCK_DGRAM)
        self.address = (host, port)

    def run(self):
        self.client.connect()
        self.client.run(callback=self.process_beacon, autoreconnect=True)

    def disconnect(self):
        self.client.disconnect()
