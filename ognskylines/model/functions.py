from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from geoalchemy2.functions import ST_Distance_Sphere

from ognskylines.dbutils import session
from ognskylines.model import Location, Device, User


def validate_ogn_address(ogn_address):
    if not len(ogn_address) == 6:
        raise ValueError('no valid ogn_address given')
    try:
        int(ogn_address, 16)
    except ValueError:
        raise ValueError('no valid skylines_key given (hexadecimal string)')


def validate_skylines_key(skylines_key):
    if not len(skylines_key) == 8:
        raise ValueError('no valid skylines_key given')
    try:
        int(skylines_key, 16)
    except ValueError:
        raise ValueError('no valid skylines_key given (hexadecimal string)')


def insert_user(skylines_key, ogn_address, add_device=False):
    """
    Arguments:
    skylines_key -- hexadecimal string (4 bytes)
    ogn_address  -- hexadecimal string (3 bytes)
    add_device   -- boolean

    raises:
    NoResultFound
    IntegrityError
    """

    validate_skylines_key(skylines_key)
    validate_ogn_address(ogn_address)

    try:
        session.query(Device).filter(Device.ogn_address == ogn_address).one()
    except NoResultFound as e:
        if not add_device:
            raise e
        else:
            device = Device(ogn_address=ogn_address)
            session.add(device)

    user = User(ogn_address=ogn_address, skylines_key=int(skylines_key, 16))
    try:
        session.add(user)
        session.commit()
    except IntegrityError as e:
        raise e
    return user


def delete_user(skylines_key):
    """
    Arguments:
    skylines_key -- hexadecimal string (4 bytes)

    raises:
    NoResultFound
    """

    validate_skylines_key(skylines_key)

    try:
        query = session.query(User).filter(User.skylines_key == int(skylines_key, 16))
        users = query.all()
        query.delete()
        session.commit()
    except NoResultFound as e:
        raise e
    return users


def show_user(skylines_key):
    """
    Arguments:
    skylines_key -- hexadecimal string (4 bytes)

    raises:
    NoResultFound
    """

    validate_skylines_key(skylines_key)

    try:
        users = session.query(User).filter(User.skylines_key == int(skylines_key, 16)).all()
    except NoResultFound as e:
        raise e
    return users


def show_users():
    """
    raises:
    NoResultFound
    """

    try:
        users = session.query(User).all()
    except NoResultFound as e:
        raise e
    return users


def get_nearby_devices(lat, lon, r, n):
    """
    Return nearby devices.

    Arguments:
    lat - Latitude in degrees
    lon - Longitude in degrees
    r   - Search radius in km
    n   - output list length limit
    """

    user_location = Location(lon=lon, lat=lat).to_wkt()
    distance = ST_Distance_Sphere(Device.location_wkb, user_location) / 1000
    direction = func.degrees(func.ST_Azimuth(user_location, Device.location_wkb))
    devices = session.query(Device,
                            direction.label('direction'),
                            distance.label('distance')).filter(distance < r).order_by(distance.asc()).limit(n).all()
    return devices
