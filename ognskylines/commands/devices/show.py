from ognskylines.dbutils import session
from ognskylines.model import Device
from ognskylines.model.device import Location
from sqlalchemy import func
from geoalchemy2.functions import ST_Distance_Sphere
from formatter import format_fuzzy_direction, format_distance

from manager import Manager
manager = Manager()


@manager.command
def show_all():
    """Show all devices with known location."""
    devices = session.query(Device).filter(Device.timestamp != None).all()  # noqa

    if len(devices) == 0:
        print('No devices with location in the databse.')
        return

    print('{:^11} | {:^23}'.format('ogn address', 'Location'))
    print('{:-<11} | {:-<23}'.format('', ''))
    for device in devices:
        print("{:>11} | {}".format(
            device.ogn_address,
            device.location))


@manager.arg('lat', help='Latitude of your location')
@manager.arg('lon', help='Longitude of your location')
@manager.arg('r', help='Search radius in km')
@manager.arg('n', help='Limit output to N entries')
@manager.command
def show_nearby(lat=49.73, lon=7.33, r=8, n=10):
    """Show nearby devices."""
    if not (lon and lat and r):
        print("Missing arguments lon/lat.")
    r = float(r) * 1000
    lat = float(lat)
    lon = float(lon)
    user_location = Location(lon=lon, lat=lat).to_wkt()
    distance = ST_Distance_Sphere(Device.location_wkb, user_location)
    direction = func.degrees(func.ST_Azimuth(user_location, Device.location_wkb))
    devices = session.query(Device, direction.label('direction'), distance.label('distance')).filter(distance < r).order_by(distance.asc()).limit(n).all()

    print('\nYour location: {}'.format(Location(lat=lat, lon=lon)))
    print('Search radius: {}\n'.format(format_distance(r)))

    if len(devices) == 0:
        print('(No devices nearby) \n\nYou may want to increase the search radius r.')
        return

    print('{:^11} | {:^18} | {}'.format('ogn address', 'Location', 'distance / bearing'))
    print('{:-<11} | {:-<18} | {:-<18}'.format('', '', ''))
    for device in devices:

        print("{:>11} | {} | {:>10}   {:>2}".format(
            device.Device.ogn_address,
            device.Device.location,
            format_distance(device.distance),
            format_fuzzy_direction(device.direction)))
