from sqlalchemy import Column, BigInteger, String

from .base import Base


class User(Base):
    __tablename__ = 'user'

    ogn_address = Column(String(6), primary_key=True)
    skylines_key = Column(BigInteger, nullable=False)

    @property
    def skylines_key_hex(self):
        if self.skylines_key is None:
            return None

        return '{:X}'.format(self.skylines_key)

    def __repr__(self):
        return str(self.as_dict())

    def as_dict(self):
        return {'ogn_address': self.ogn_address,
                'skylines_key': self.skylines_key_hex}
