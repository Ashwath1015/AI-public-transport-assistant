import os
from sqlalchemy import text
from database import engine, SessionLocal

def seed_data():
    session = SessionLocal()
    try:
        print("Seeding sample transit data...")

        # 1. Insert Sample Stops
        stops = [
            ("S1", "Anna Nagar", 13.0850, 80.2450),
            ("S2", "Central", 13.0827, 80.2707),
            ("S3", "T Nagar", 13.0418, 80.2341),
            ("S4", "Velachery", 12.9654, 80.2173),
        ]

        for stop_id, name, lat, lon in stops:
            session.execute(text("""
                INSERT INTO stops (stop_id, stop_name, stop_lat, stop_lon, location)
                VALUES (:id, :name, :lat, :lon, ST_GeomFromText(:geom, 4326))
                ON CONFLICT (stop_id) DO NOTHING
            """), {"id": stop_id, "name": name, "lat": lat, "lon": lon, "geom": f"POINT({lon} {lat})"})

        # 2. Insert a Route
        session.execute(text("""
            INSERT INTO routes (route_id, route_short_name, route_long_name, route_type)
            VALUES ('R1', '101', 'Anna Nagar to Central Express', 3)
            ON CONFLICT (route_id) DO NOTHING
        """))

        # 3. Insert a Trip
        session.execute(text("""
            INSERT INTO trips (trip_id, route_id, service_id)
            VALUES ('T1', 'R1', 'S1')
            ON CONFLICT (trip_id) DO NOTHING
        """))

        # 4. Insert Stop Times (The actual path)
        # Trip T1: Anna Nagar (S1) -> Central (S2)
        stop_times = [
            ('T1', 'S1', '08:00', '08:05', 1),
            ('T1', 'S2', '08:20', '08:25', 2),
        ]
        for tid, sid, arr, dep, seq in stop_times:
            session.execute(text("""
                INSERT INTO stop_times (trip_id, stop_id, arrival_time, departure_time, stop_sequence)
                VALUES (:tid, :sid, :at, :dt, :ss)
                ON CONFLICT DO NOTHING
            """), {"tid": tid, "sid": sid, "at": arr, "dt": dep, "ss": seq})

        session.commit()
        print("Sample data seeded successfully!")
        print("\nTry searching from 'Anna Nagar' to 'Central' in the app!")

    except Exception as e:
        print(f"Error seeding data: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    seed_data()
