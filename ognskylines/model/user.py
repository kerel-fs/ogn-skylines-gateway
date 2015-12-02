from sqlalchemy import Column, BigInteger, String

from .base import Base


class User(Base):
    __tablename__ = 'user'

    ogn_address = Column(String(6), primary_key=True)
    skylines_key = Column(BigInteger, nullable=False)

    def __repr__(self):
        return "<User: %s,%s>" % (
            self.ogn_address,
            self.skylines_key)
