from sqlalchemy import text
from database import SessionLocal

def debug_db():
    session = SessionLocal()
    try:
        print("--- Database Debug Info ---")

        print("\n[Stops]")
        stops = session.execute(text("SELECT stop_id, stop_name FROM stops")).fetchall()
        for s in stops: print(f"ID: {s[0]}, Name: {s[1]}")

        print("\n[Routes]")
        routes = session.execute(text("SELECT route_id, route_short_name FROM routes")).fetchall()
        for r in routes: print(f"ID: {r[0]}, ShortName: {r[1]}")

        print("\n[Trips]")
        trips = session.execute(text("SELECT trip_id, route_id FROM trips")).fetchall()
        for t in trips: print(f"ID: {t[0]}, RouteID: {t[1]}")

        print("\n[Stop Times]")
        st = session.execute(text("SELECT trip_id, stop_id, stop_sequence FROM stop_times ORDER BY trip_id, stop_sequence")).fetchall()
        for s in st: print(f"Trip: {s[0]}, Stop: {s[1]}, Seq: {s[2]}")

        print("\n--- End Debug Info ---")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    debug_db()
