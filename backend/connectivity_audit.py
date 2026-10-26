from database import SessionLocal
from sqlalchemy import text

def audit_connectivity():
    session = SessionLocal()
    try:
        # 1. Get Ashok Nagar ID
        stop = session.execute(
            text("SELECT stop_id FROM stops WHERE stop_name ILIKE :name LIMIT 1"), 
            {"name": "%Ashok Nagar%"}
        ).fetchone()
        
        if not stop:
            print("Error: Ashok Nagar not found.")
            return
        
        origin_id = stop[0]
        print(f"Audit Origin: Ashok Nagar ({origin_id})")
        
        # 2. Find all stops reachable in 1 hop (same trip)
        reachable_stops = set()
        trips = session.execute(
            text("SELECT trip_id FROM stop_times WHERE stop_id = :sid"), 
            {"sid": origin_id}
        ).fetchall()
        
        print(f"Found {len(trips)} trips passing through Ashok Nagar.")
        
        for (tid,) in trips:
            res = session.execute(
                text("SELECT stop_id FROM stop_times WHERE trip_id = :tid"), 
                {"tid": tid}
            ).fetchall()
            for (sid,) in res:
                reachable_stops.add(sid)
        
        print(f"Unique stops reachable in 1 hop: {len(reachable_stops)}")
        
        # 3. See if any of these are hubs
        hubs = session.execute(
            text("SELECT stop_id, stop_name FROM stops WHERE stop_name ILIKE '%Central%' OR stop_name ILIKE '%T Nagar%'")
        ).fetchall()
        
        found_hub = False
        for hub_id, hub_name in hubs:
            if hub_id in reachable_stops:
                print(f"SUCCESS: Ashok Nagar is directly connected to {hub_name}!")
                found_hub = True
        
        if not found_hub:
            print("FAIL: Ashok Nagar is not directly connected to any major hub in the current data.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    audit_connectivity()
