from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata

# Location Model
class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    region = Column(String, nullable=False)  # e.g., "Phuket" or "Krabi"

    accommodations = relationship("Accommodation", back_populates="location")
    transfers_from = relationship("Transfer", foreign_keys="[Transfer.from_location_id]", back_populates="from_location")
    transfers_to = relationship("Transfer", foreign_keys="[Transfer.to_location_id]", back_populates="to_location")
    activities = relationship("Activity", back_populates="location")

# Accommodation Model
class Accommodation(Base):
    __tablename__ = "accommodations"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)

    location = relationship("Location", back_populates="accommodations")
    days = relationship("Day", back_populates="accommodation")

# Transfer Model
class Transfer(Base):
    __tablename__ = "transfers"
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)  # e.g., "ferry", "car"
    from_location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    to_location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    duration = Column(Integer, nullable=False)  # in minutes

    from_location = relationship("Location", foreign_keys=[from_location_id], back_populates="transfers_from")
    to_location = relationship("Location", foreign_keys=[to_location_id], back_populates="transfers_to")
    day_transfers = relationship("DayTransfer", back_populates="transfer")

# Activity Model
class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    duration = Column(Integer, nullable=False)  # in minutes

    location = relationship("Location", back_populates="activities")
    day_activities = relationship("DayActivity", back_populates="activity")

# Itinerary Model
class Itinerary(Base):
    __tablename__ = "itineraries"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    total_nights = Column(Integer, nullable=False)

    days = relationship("Day", back_populates="itinerary")

# Day Model
class Day(Base):
    __tablename__ = "days"
    id = Column(Integer, primary_key=True)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id"), nullable=False)
    day_number = Column(Integer, nullable=False)
    accommodation_id = Column(Integer, ForeignKey("accommodations.id"), nullable=False)

    itinerary = relationship("Itinerary", back_populates="days")
    accommodation = relationship("Accommodation", back_populates="days")
    day_transfers = relationship("DayTransfer", back_populates="day")
    day_activities = relationship("DayActivity", back_populates="day")

# DayTransfer Model (Junction Table)
class DayTransfer(Base):
    __tablename__ = "day_transfers"
    id = Column(Integer, primary_key=True)
    day_id = Column(Integer, ForeignKey("days.id"), nullable=False)
    transfer_id = Column(Integer, ForeignKey("transfers.id"), nullable=False)
    scheduled_time = Column(DateTime, nullable=False)

    day = relationship("Day", back_populates="day_transfers")
    transfer = relationship("Transfer", back_populates="day_transfers")

# DayActivity Model (Junction Table)
class DayActivity(Base):
    __tablename__ = "day_activities"
    id = Column(Integer, primary_key=True)
    day_id = Column(Integer, ForeignKey("days.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    scheduled_time = Column(DateTime, nullable=False)

    day = relationship("Day", back_populates="day_activities")
    activity = relationship("Activity", back_populates="day_activities")