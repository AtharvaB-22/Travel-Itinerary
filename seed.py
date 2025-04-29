from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from models import Base, Location, Accommodation, Transfer, Activity, Itinerary, Day, DayTransfer, DayActivity
from datetime import datetime

# Setup database connection
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Clear existing data for a fresh seed (optional)
session.query(DayTransfer).delete()
session.query(DayActivity).delete()
session.query(Day).delete()
session.query(Itinerary).delete()
session.query(Activity).delete()
session.query(Transfer).delete()
session.query(Accommodation).delete()
session.query(Location).delete()
session.commit()

# Seed Locations
locations = [
    Location(name="Patong Beach", region="Phuket"),
    Location(name="Kata Beach", region="Phuket"),
    Location(name="Phi Phi Islands", region="Phuket"),
    Location(name="Ao Nang", region="Krabi"),
    Location(name="Railay Beach", region="Krabi"),
]
session.add_all(locations)
session.commit()

# Seed Accommodations
accommodations = [
    Accommodation(name="Centara Grand", location_id=1),  # Patong Beach
    Accommodation(name="Kata Palm Resort", location_id=2),  # Kata Beach
    Accommodation(name="Phi Phi Island Village", location_id=3),  # Phi Phi Islands
    Accommodation(name="Aonang Cliff Beach Resort", location_id=4),  # Ao Nang
    Accommodation(name="Rayavadee", location_id=5),  # Railay Beach
]
session.add_all(accommodations)
session.commit()

# Seed Transfers
transfers = [
    Transfer(type="ferry", from_location_id=1, to_location_id=3, duration=120),  # Patong to Phi Phi
    Transfer(type="car", from_location_id=1, to_location_id=2, duration=30),  # Patong to Kata
    Transfer(type="ferry", from_location_id=3, to_location_id=4, duration=90),  # Phi Phi to Ao Nang
    Transfer(type="car", from_location_id=4, to_location_id=5, duration=20),  # Ao Nang to Railay
]
session.add_all(transfers)
session.commit()

# Seed Activities
activities = [
    Activity(name="Snorkeling Tour", location_id=1, duration=180),  # Patong Beach
    Activity(name="Scuba Diving", location_id=2, duration=240),  # Kata Beach
    Activity(name="Island Hopping", location_id=3, duration=300),  # Phi Phi Islands
    Activity(name="Rock Climbing", location_id=5, duration=120),  # Railay Beach
    Activity(name="Kayaking", location_id=4, duration=150),  # Ao Nang
]
session.add_all(activities)
session.commit()

# Seed Itineraries
itineraries = [
    Itinerary(name="Phuket Getaway", start_date=datetime(2023, 12, 1), total_nights=2, recommended_for_nights=2),
    Itinerary(name="Krabi Adventure", start_date=datetime(2023, 12, 5), total_nights=3, recommended_for_nights=3),
    Itinerary(name="Phuket-Krabi Combo", start_date=datetime(2023, 12, 10), total_nights=5, recommended_for_nights=5),
    Itinerary(name="Ultimate Thailand Tour", start_date=datetime(2023, 12, 15), total_nights=8, recommended_for_nights=8),
]
session.add_all(itineraries)
session.commit()

# Seed Days for Itineraries
# Phuket Getaway (2 nights)
itinerary1 = session.query(Itinerary).filter_by(name="Phuket Getaway").first()
days_itinerary1 = [
    Day(itinerary_id=itinerary1.id, day_number=1, accommodation_id=1),  # Centara Grand, Patong
    Day(itinerary_id=itinerary1.id, day_number=2, accommodation_id=2),  # Kata Palm Resort, Kata
]
session.add_all(days_itinerary1)

# Krabi Adventure (3 nights)
itinerary2 = session.query(Itinerary).filter_by(name="Krabi Adventure").first()
days_itinerary2 = [
    Day(itinerary_id=itinerary2.id, day_number=1, accommodation_id=4),  # Aonang Cliff Beach Resort, Ao Nang
    Day(itinerary_id=itinerary2.id, day_number=2, accommodation_id=5),  # Rayavadee, Railay
    Day(itinerary_id=itinerary2.id, day_number=3, accommodation_id=4),  # Back to Aonang Cliff Beach Resort
]
session.add_all(days_itinerary2)

# Phuket-Krabi Combo (5 nights)
itinerary3 = session.query(Itinerary).filter_by(name="Phuket-Krabi Combo").first()
days_itinerary3 = [
    Day(itinerary_id=itinerary3.id, day_number=1, accommodation_id=1),  # Centara Grand, Patong
    Day(itinerary_id=itinerary3.id, day_number=2, accommodation_id=2),  # Kata Palm Resort, Kata
    Day(itinerary_id=itinerary3.id, day_number=3, accommodation_id=3),  # Phi Phi Island Village, Phi Phi
    Day(itinerary_id=itinerary3.id, day_number=4, accommodation_id=4),  # Aonang Cliff Beach Resort, Ao Nang
    Day(itinerary_id=itinerary3.id, day_number=5, accommodation_id=5),  # Rayavadee, Railay
]
session.add_all(days_itinerary3)

# Ultimate Thailand Tour (8 nights)
itinerary4 = session.query(Itinerary).filter_by(name="Ultimate Thailand Tour").first()
days_itinerary4 = [
    Day(itinerary_id=itinerary4.id, day_number=1, accommodation_id=1),  # Centara Grand, Patong
    Day(itinerary_id=itinerary4.id, day_number=2, accommodation_id=2),  # Kata Palm Resort, Kata
    Day(itinerary_id=itinerary4.id, day_number=3, accommodation_id=2),  # Kata Palm Resort, Kata
    Day(itinerary_id=itinerary4.id, day_number=4, accommodation_id=3),  # Phi Phi Island Village, Phi Phi
    Day(itinerary_id=itinerary4.id, day_number=5, accommodation_id=3),  # Phi Phi Island Village, Phi Phi
    Day(itinerary_id=itinerary4.id, day_number=6, accommodation_id=4),  # Aonang Cliff Beach Resort, Ao Nang
    Day(itinerary_id=itinerary4.id, day_number=7, accommodation_id=5),  # Rayavadee, Railay
    Day(itinerary_id=itinerary4.id, day_number=8, accommodation_id=5),  # Rayavadee, Railay
]
session.add_all(days_itinerary4)
session.commit()

# Seed DayTransfers and DayActivities
# Phuket Getaway
day1_itinerary1 = session.query(Day).filter_by(itinerary_id=itinerary1.id, day_number=1).first()
day2_itinerary1 = session.query(Day).filter_by(itinerary_id=itinerary1.id, day_number=2).first()
session.add(DayTransfer(day_id=day2_itinerary1.id, transfer_id=2, scheduled_time=datetime(2023, 12, 2, 10, 0)))  # Car to Kata
session.add(DayActivity(day_id=day1_itinerary1.id, activity_id=1, scheduled_time=datetime(2023, 12, 1, 14, 0)))  # Snorkeling

# Krabi Adventure
day2_itinerary2 = session.query(Day).filter_by(itinerary_id=itinerary2.id, day_number=2).first()
session.add(DayTransfer(day_id=day2_itinerary2.id, transfer_id=4, scheduled_time=datetime(2023, 12, 6, 9, 0)))  # Car to Railay
session.add(DayActivity(day_id=day2_itinerary2.id, activity_id=4, scheduled_time=datetime(2023, 12, 6, 13, 0)))  # Rock Climbing

# Phuket-Krabi Combo
day3_itinerary3 = session.query(Day).filter_by(itinerary_id=itinerary3.id, day_number=3).first()
day4_itinerary3 = session.query(Day).filter_by(itinerary_id=itinerary3.id, day_number=4).first()
session.add(DayTransfer(day_id=day3_itinerary3.id, transfer_id=1, scheduled_time=datetime(2023, 12, 12, 8, 0)))  # Ferry to Phi Phi
session.add(DayTransfer(day_id=day4_itinerary3.id, transfer_id=3, scheduled_time=datetime(2023, 12, 13, 10, 0)))  # Ferry to Ao Nang
session.add(DayActivity(day_id=day3_itinerary3.id, activity_id=3, scheduled_time=datetime(2023, 12, 12, 13, 0)))  # Island Hopping

# Ultimate Thailand Tour
day4_itinerary4 = session.query(Day).filter_by(itinerary_id=itinerary4.id, day_number=4).first()
session.add(DayTransfer(day_id=day4_itinerary4.id, transfer_id=1, scheduled_time=datetime(2023, 12, 18, 9, 0)))  # Ferry to Phi Phi
session.add(DayActivity(day_id=day4_itinerary4.id, activity_id=3, scheduled_time=datetime(2023, 12, 18, 13, 0)))  # Island Hopping

session.commit()

# Close session
session.close()

print("Database seeding completed successfully!")