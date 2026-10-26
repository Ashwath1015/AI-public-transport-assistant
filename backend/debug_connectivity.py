from database import SessionLocal
from sqlalchemy import text

def check_stop(stop_name):
    session = SessionLocal()
    try:
        print(f"--- Debugging Connectivity for: {stop_name} ---")
        
        # 1. Find the stop ID
        stop = session.execute(
            text("SELECT stop_id FROM stops WHERE stop_name ILIKE :name LIMIT 1"), 
            {"name": f"%{stop_name}%"}
        ).fetchone()
        
        if not stop:
            print(f"Stop '{stop_name}' not found in database.")
            return
        
        stop_id = stop[0]
        print(f"Found Stop: {stop_name} (ID: {stop_id})")
        
        # 2. Check for stop times
        st_count = session.execute(
            text("SELECT count(*) FROM stop_times WHERE stop_id = :sid"), 
            {"sid": stop_id}
        ).scalar()
        
        print(f"Stop Times count: {st_count}")
        if st_count == 0:
            print("This stop has NO scheduled arrivals/departures in stop_times table.")
            return
        
        # 3. Check which trips pass through here
        trips = session.execute(
            text("""
                SELECT t.trip_id, r.route_short_name, r.route_long_name 
                FROM stop_times st 
                JOIN trips t ON st.trip_id = t.trip_id 
                JOIN routes r ON t.route_id = r.route_id 
                WHERE st.stop_id = :sid 
                LIMIT 5
            """), {"sid": stop_id}
        ).fetchall()
        
        print("Trips passing through this stop:")
        for trip in trips:
            print(f" - Trip {trip[0]} (Route {trip[1]}: {trip[2]})")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    check_stop("Ashok Nagar")
