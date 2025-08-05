from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.session import Base

# Ассоциативная таблица для связи организаций и номеров телефонов
organization_phone = Table(
    'organization_phone', Base.metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id')),
    Column('phone_id', Integer, ForeignKey('phones.id'))
)

# Ассоциативная таблица для связи организаций и видов деятельности
organization_activity = Table(
    'organization_activity', Base.metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id')),
    Column('activity_id', Integer, ForeignKey('activities.id'))
)

class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    building_id = Column(Integer, ForeignKey('buildings.id'))

    phones = relationship("Phone", secondary=organization_phone, back_populates="organizations")
    activities = relationship("Activity", secondary=organization_activity, back_populates="organizations")
    building = relationship("Building", back_populates="organizations")

class Phone(Base):
    __tablename__ = 'phones'

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String)

    organizations = relationship("Organization", secondary=organization_phone, back_populates="phones")
