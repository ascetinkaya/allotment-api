from database import SessionLocal, engine, Base
from models import Hotel, RoomType, Partner

Base.metadata.create_all(bind=engine)

db = SessionLocal()

if db.query(Hotel).count() == 0:
    hotel1 = Hotel(name="TestHotel-1", city="Istanbul", country="Turkey", address="Fatih, Istanbul")
    hotel2 = Hotel(name="TestHotel-2", city="Ankara", country="Turkey", address="Kızılay, Ankara")
    hotel3 = Hotel(name="TestHotel-3", city="Istanbul", country="Turkey", address="Beşiktaş, Istanbul")
    hotel4 = Hotel(name="TestHotel-4", city="London", country="United Kingdom", address="Camden Town, London")
    hotel5 = Hotel(name="TestHotel-5", city="Seville", country="Spain", address="La calle test, Seville")

    db.add_all([hotel1, hotel2, hotel3, hotel4, hotel5])
    db.commit()
    db.refresh(hotel1)
    db.refresh(hotel2)
    db.refresh(hotel3)
    db.refresh(hotel4)
    db.refresh(hotel5)

    rooms = [
        RoomType(hotel_id=hotel1.id, name="Standard Room", max_occupancy=2, price_per_night=100.0, total_inventory=10),
        RoomType(hotel_id=hotel1.id, name="Deluxe Room", max_occupancy=2, price_per_night=200.0, total_inventory=5),
        RoomType(hotel_id=hotel1.id, name="Suite", max_occupancy=4, price_per_night=300.0, total_inventory=2),
        RoomType(hotel_id=hotel2.id, name="Standard Room", max_occupancy=2, price_per_night=90.0, total_inventory=15),
        RoomType(hotel_id=hotel2.id, name="Executive Room", max_occupancy=2, price_per_night=180.0, total_inventory=8),
        RoomType(hotel_id=hotel3.id, name="Standard Room", max_occupancy=2, price_per_night=100.0, total_inventory=10),
        RoomType(hotel_id=hotel4.id, name="Deluxe Room", max_occupancy=2, price_per_night=140.0, total_inventory=5),
        RoomType(hotel_id=hotel5.id, name="Standard Room", max_occupancy=2, price_per_night=80.0, total_inventory=12),
    ]

    db.add_all(rooms)
    db.commit()
    print("Seed data added successfully!")
else:
    print("Database already seeded, skipping.")
if db.query(Partner).count() == 0:
    partners = [
        Partner(name="Partner A", api_key="test-key-partner-a", is_active=True),
        Partner(name="Partner B", api_key="test-key-partner-b", is_active=True),
    ]
    db.add_all(partners)
    db.commit()
    print("Partners seeded successfully!")

db.close()