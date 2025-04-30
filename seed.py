from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from models import Base, Location, Accommodation, Transfer, Activity, Itinerary, Day, DayTransfer, DayActivity
from datetime import datetime

# Setup database connection
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Clear existing data for a fresh seed
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

# Seed Itineraries (covering 2-8 nights)
itineraries = [
    Itinerary(name="Phuket Getaway", start_date=datetime(2023, 12, 1), total_nights=2, recommended_for_nights=2),
    Itinerary(name="Krabi Adventure", start_date=datetime(2023, 12, 5), total_nights=3, recommended_for_nights=3),
    Itinerary(name="Phuket Explorer", start_date=datetime(2023, 12, 8), total_nights=4, recommended_for_nights=4),
    Itinerary(name="Phuket-Krabi Combo", start_date=datetime(2023, 12, 10), total_nights=5, recommended_for_nights=5),
    Itinerary(name="Phuket Extended", start_date=datetime(2023, 12, 15), total_nights=6, recommended_for_nights=6),
    Itinerary(name="Krabi Extended", start_date=datetime(2023, 12, 20), total_nights=7, recommended_for_nights=7),
    Itinerary(name="Ultimate Thailand Tour", start_date=datetime(2023, 12, 25), total_nights=8, recommended_for_nights=8),
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

# Phuket Explorer (4 nights)
itinerary3 = session.query(Itinerary).filter_by(name="Phuket Explorer").first()
days_itinerary3 = [
    Day(itinerary_id=itinerary3.id, day_number=1, accommodation_id=1),  # Centara Grand, Patong
    Day(itinerary_id=itinerary3.id, day_number=2, accommodation_id=2),  # Kata Palm Resort, Kata
    Day(itinerary_id=itinerary3.id, day_number=3, accommodation_id=3),  # Phi Phi Island Village, Phi Phi
    Day(itinerary_id=itinerary3.id, day_number=4, accommodation_id=1),  # Back to Centara Grand, Patong
]
session.add_all(days_itinerary3)

# Phuket-Krabi Combo (5 nights)
itinerary4 = session.query(Itinerary).filter_by(name="Phuket-Krabi Combo").first()
days_itinerary4 = [
    Day(itinerary_id=itinerary4.id, day_number=1, accommodation_id=1),  # Centara Grand, Patong
    Day(itinerary_id=itinerary4.id, day_number=2, accommodation_id=2),  # Kata Palm Resort, Kata
    Day(itinerary_id=itinerary4.id, day_number=3, accommodation_id=3),  # Phi Phi Island Village, Phi Phi
    Day(itinerary_id=itinerary4.id, day_number=4, accommodation_id=4),  # Aonang Cliff Beach Resort, Ao Nang
    Day(itinerary_id=itinerary4.id, day_number=5, accommodation_id=5),  # Rayavadee, Railay
]
session.add_all(days_itinerary4)

# Phuket Extended (6 nights)
itinerary5 = session.query(Itinerary).filter_by(name="Phuket Extended").first()
days_itinerary5 = [
    Day(itinerary_id=itinerary5.id, day_number=1, accommodation_id=1),  # Centara Grand, Patong
    Day(itinerary_id=itinerary5.id, day_number=2, accommodation_id=2),  # Kata Palm Resort, Kata
    Day(itinerary_id=itinerary5.id, day_number=3, accommodation_id=2),  # Kata Palm Resort, Kata
    Day(itinerary_id=itinerary5.id, day_number=4, accommodation_id=3),  # Phi Phi Island Village, Phi Phi
    Day(itinerary_id=itinerary5.id, day_number=5, accommodation_id=3),  # Phi Phi Island Village, Phi Phi
    Day(itinerary_id=itinerary5.id, day_number=6, accommodation_id=1),  # Back to Centara Grand, Patong
]
session.add_all(days_itinerary5)

# Krabi Extended (7 nights)
itinerary6 = session.query(Itinerary).filter_by(name="Krabi Extended").first()
days_itinerary6 = [
    Day(itinerary_id=itinerary6.id, day_number=1, accommodation_id=4),  # Aonang Cliff Beach Resort, Ao Nang
    Day(itinerary_id=itinerary6.id, day_number=2, accommodation_id=5),  # Rayavadee, Railay
    Day(itinerary_id=itinerary6.id, day_number=3, accommodation_id=5),  # Rayavadee, Railay
    Day(itinerary_id=itinerary6.id, day_number=4, accommodation_id=4),  # Aonang Cliff Beach Resort, Ao Nang
    Day(itinerary_id=itinerary6.id, day_number=5, accommodation_id=4),  # Aonang Cliff Beach Resort, Ao Nang
    Day(itinerary_id=itinerary6.id, day_number=6, accommodation_id=5),  # Rayavadee, Railay
    Day(itinerary_id=itinerary6.id, day_number=7, accommodation_id=4),  # Back to Aonang Cliff Beach Resort
]
session.add_all(days_itinerary6)

# Ultimate Thailand Tour (8 nights)
itinerary7 = session.query(Itinerary).filter_by(name="Ultimate Thailand Tour").first()
days_itinerary7 = [
    Day(itinerary_id=itinerary7.id, day_number=1, accommodation_id=1),  # Centara Grand, Patong
    Day(itinerary_id=itinerary7.id, day_number=2, accommodation_id=2),  # Kata Palm Resort, Kata
    Day(itinerary_id=itinerary7.id, day_number=3, accommodation_id=2),  # Kata Palm Resort, Kata
    Day(itinerary_id=itinerary7.id, day_number=4, accommodation_id=3),  # Phi Phi Island Village, Phi Phi
    Day(itinerary_id=itinerary7.id, day_number=5, accommodation_id=3),  # Phi Phi Island Village, Phi Phi
    Day(itinerary_id=itinerary7.id, day_number=6, accommodation_id=4),  # Aonang Cliff Beach Resort, Ao Nang
    Day(itinerary_id=itinerary7.id, day_number=7, accommodation_id=5),  # Rayavadee, Railay
    Day(itinerary_id=itinerary7.id, day_number=8, accommodation_id=5),  # Rayavadee, Railay
]
session.add_all(days_itinerary7)
session.commit()

# Seed DayTransfers and DayActivities (simplified for brevity)
session.commit()

# Close session
session.close()

print("Database seeding completed successfully!")