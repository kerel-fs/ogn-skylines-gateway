from sqlalchemy import Column, DateTime, String
from geoalchemy2.types import Geometry
from geoalchemy2.shape import to_shape, from_shape
from shapely.geometry import Point

from .base import Base


class Location:
    """Represents a location in WGS84"""

    def __init__(self, lon, lat):
        self.longitude = lon
        self.latitude = lat

    def to_wkt(self):
        return 'SRID=4326;POINT({0} {1})'.format(self.longitude, self.latitude)

    def __str__(self):
        return '{0: 7.4f}, {1:8.4f}'.format(self.latitude, self.longitude)

    def as_dict(self):
        return {'latitude': round(self.latitude, 8), 'longitude': round(self.longitude, 8)}


class Device(Base):
    __tablename__ = 'device'

    ogn_address = Column(String(6), primary_key=True)
    timestamp = Column(DateTime)
    location_wkb = Column('location', Geometry('POINT', srid=4326))

    @property
    def location(self):
        if self.location_wkb is None:
            return None

        shape = to_shape(self.location_wkb)
        return Location(lat=shape.y, lon=shape.x)

    def set_location(self, longitude, latitude):
        self.location_wkb = from_shape(Point(longitude, latitude), srid=4326)

    def __repr__(self):
        return str(self.as_dict())

    def as_dict(self):
        return {'ogn_address': '{}'.format(self.ogn_address),
                'timestamp': '{}'.format(self.timestamp),
                'location': self.location.as_dict()}
