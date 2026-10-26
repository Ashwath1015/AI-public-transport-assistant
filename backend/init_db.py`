import os
from sqlalchemy import text
from database import engine, SessionLocal

def init_db():
    session = SessionLocal()
    try:
        print("Creating tables...")
        # Create PostGIS extension if not exists
        session.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))

        # Stops Table
        session.execute(text("""
            CREATE TABLE IF NOT EXISTS stops (
                stop_id TEXT PRIMARY KEY,
                stop_name TEXT NOT NULL,
                stop_lat DOUBLE PRECISION,
                stop_lon DOUBLE PRECISION,
                location GEOGRAPHY(Point, 4326)
            );
        """))

        # Routes Table
        session.execute(text("""
            CREATE TABLE IF NOT EXISTS routes (
                route_id TEXT PRIMARY KEY,
                route_short_name TEXT,
                route_long_name TEXT,
                route_type INTEGER
            );
        """))

        # Calendar Table
        session.execute(text("""
            CREATE TABLE IF NOT EXISTS calendar (
                service_id TEXT PRIMARY KEY,
                start_date DATE,
                end_date DATE
            );
        """))

        # Trips Table
        session.execute(text("""
            CREATE TABLE IF NOT EXISTS trips (
                trip_id TEXT PRIMARY KEY,
                route_id TEXT,
                service_id TEXT
            );
        """))

        # Stop Times Table
        session.execute(text("""
            CREATE TABLE IF NOT EXISTS stop_times (
                trip_id TEXT,
                stop_id TEXT,
                arrival_time TEXT,
                departure_time TEXT,
                stop_sequence INTEGER,
                PRIMARY KEY (trip_id, stop_sequence)
            );
        """))

        session.commit()
        print("All tables created successfully!")

    except Exception as e:
        print(f"Error creating tables: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    init_db()
