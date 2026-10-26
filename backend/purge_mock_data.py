from database import SessionLocal
from sqlalchemy import text

def purge():
    session = SessionLocal()
    try:
        print("Purging mock seed data...")
        
        # Delete in order to respect Foreign Key constraints
        session.execute(text("DELETE FROM stop_times WHERE trip_id = 'T1' OR stop_id IN ('S1', 'S2', 'S3', 'S4')"))
        session.execute(text("DELETE FROM trips WHERE trip_id = 'T1'"))
        session.execute(text("DELETE FROM routes WHERE route_id = 'R1'"))
        session.execute(text("DELETE FROM stops WHERE stop_id IN ('S1', 'S2', 'S3', 'S4')"))
        
        session.commit()
        print("Mock data purged successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    purge()
