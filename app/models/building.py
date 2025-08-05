from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base

class Building(Base):
    __tablename__ = 'buildings'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    latitude = Column(String)
    longitude = Column(String)

    organizations = relationship("Organization", back_populates="building")
