from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Hotel(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    address = Column(String)
    rooms = relationship("RoomType", back_populates="hotel")

class RoomType(Base):
    __tablename__ = "room_types"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    name = Column(String, nullable=False)
    max_occupancy = Column(Integer)
    price_per_night = Column(Float)
    total_inventory = Column(Integer)
    hotel = relationship("Hotel", back_populates="rooms")
    bookings = relationship("Booking", back_populates="room_type")

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    booking_ref = Column(String, unique=True, index=True)
    room_type_id = Column(Integer, ForeignKey("room_types.id"))
    guest_name = Column(String, nullable=False)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    pax = Column(Integer)
    is_cancelled = Column(Boolean, default=False)
    room_type = relationship("RoomType", back_populates="bookings")
    partner_id = Column(Integer, ForeignKey("partners.id"), nullable=True)
    partner = relationship("Partner", back_populates="bookings")

class Partner(Base):
    __tablename__="partners"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    api_key = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    bookings = relationship("Booking", back_populates="partner")
