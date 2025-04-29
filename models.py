from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Index, UniqueConstraint
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

    # Unique constraint: No duplicate location names in the same region
    __table_args__ = (
        UniqueConstraint('name', 'region', name='uix_location_name_region'),
        Index('idx_location_region', 'region'),  # Index for faster queries by region
    )

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

    # Index on foreign key for faster joins
    __table_args__ = (
        Index('idx_accommodation_location_id', 'location_id'),
    )

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

    # Indexes on foreign keys
    __table_args__ = (
        Index('idx_transfer_from_location_id', 'from_location_id'),
        Index('idx_transfer_to_location_id', 'to_location_id'),
    )

    from_location = relationship("Location", foreign_keys=[from_location_id], back_populates="transfers_from")
    to_location = relationship("Location", foreign_keys=[to_location_id], back_populates="transfers_to")
    day_transfers = relationship("DayTransfer", back_populates="transfer")

# Activity Model
# filepath: d:\Full Stack Projects\Travel-Itinerary\Backend\models.py
class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    duration = Column(Integer, nullable=False)  # in minutes

    # Index on foreign key
    __table_args__ = (
        Index('idx_activity_location_id', 'location_id'),
    )

    location = relationship("Location", back_populates="activities")
    day_activities = relationship("DayActivity", back_populates="activity")  # Add this line

# Itinerary Model
class Itinerary(Base):
    __tablename__ = "itineraries"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    total_nights = Column(Integer, nullable=False)

    # Add recommended_for_nights field for MCP server (we'll use this in Step 6)
    recommended_for_nights = Column(Integer, nullable=True)

    days = relationship("Day", back_populates="itinerary")

# Day Model
# filepath: d:\Full Stack Projects\Travel-Itinerary\Backend\models.py
class Day(Base):
    __tablename__ = "days"
    id = Column(Integer, primary_key=True)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id"), nullable=False)
    day_number = Column(Integer, nullable=False)
    accommodation_id = Column(Integer, ForeignKey("accommodations.id"), nullable=False)

    # Unique constraint: One day_number per itinerary
    # Index on foreign keys
    __table_args__ = (
        UniqueConstraint('itinerary_id', 'day_number', name='uix_day_itinerary_day_number'),
        Index('idx_day_itinerary_id', 'itinerary_id'),
        Index('idx_day_accommodation_id', 'accommodation_id'),
    )

    itinerary = relationship("Itinerary", back_populates="days")
    accommodation = relationship("Accommodation", back_populates="days")
    day_transfers = relationship("DayTransfer", back_populates="day")
    day_activities = relationship("DayActivity", back_populates="day")  # Add this line

# DayTransfer Model (Junction Table)
class DayTransfer(Base):
    __tablename__ = "day_transfers"
    id = Column(Integer, primary_key=True)
    day_id = Column(Integer, ForeignKey("days.id"), nullable=False)
    transfer_id = Column(Integer, ForeignKey("transfers.id"), nullable=False)
    scheduled_time = Column(DateTime, nullable=False)

    # Index on foreign keys
    __table_args__ = (
        Index('idx_day_transfer_day_id', 'day_id'),
        Index('idx_day_transfer_transfer_id', 'transfer_id'),
    )

    day = relationship("Day", back_populates="day_transfers")
    transfer = relationship("Transfer", back_populates="day_transfers")

# filepath: d:\Full Stack Projects\Travel-Itinerary\Backend\models.py
class DayActivity(Base):
    __tablename__ = "day_activities"
    id = Column(Integer, primary_key=True)
    day_id = Column(Integer, ForeignKey("days.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    scheduled_time = Column(DateTime, nullable=False)

    # Index on foreign keys
    __table_args__ = (
        Index('idx_day_activity_day_id', 'day_id'),
        Index('idx_day_activity_activity_id', 'activity_id'),
    )

    day = relationship("Day", back_populates="day_activities")  # Ensure this matches Day model
    activity = relationship("Activity", back_populates="day_activities")  # Ensure this matches Activity model