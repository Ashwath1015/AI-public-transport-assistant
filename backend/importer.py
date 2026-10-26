import os
import zipfile
import pandas as pd
from sqlalchemy import text
from geoalchemy2.functions import ST_GeomFromText
from database import engine, SessionLocal
import argparse

def import_gtfs(zip_path):
    extract_path = "gtfs_temp"
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    session = SessionLocal()
    try:
        # 1. Stops
        print("Importing stops...")
        stops_df = pd.read_csv(f"{extract_path}/stops.txt")
        for _, row in stops_df.iterrows():
            stmt = text("""
                INSERT INTO stops (stop_id, stop_name, stop_lat, stop_lon, location)
                VALUES (:stop_id, :stop_name, :stop_lat, :stop_lon, ST_GeomFromText(:geom, 4326))
                ON CONFLICT (stop_id) DO UPDATE SET stop_name = EXCLUDED.stop_name
            """)
            session.execute(stmt, {
                "stop_id": row['stop_id'],
                "stop_name": row['stop_name'],
                "stop_lat": row['stop_lat'],
                "stop_lon": row['stop_lon'],
                "geom": f"POINT({row['stop_lon']} {row['stop_lat']})"
            })
        session.commit()

        # 2. Routes
        print("Importing routes...")
        routes_df = pd.read_csv(f"{extract_path}/routes.txt")
        for _, row in routes_df.iterrows():
            stmt = text("INSERT INTO routes (route_id, route_short_name, route_long_name, route_type) VALUES (:rid, :rsn, :rln, :rt) ON CONFLICT (route_id) DO NOTHING")
            session.execute(stmt, {"rid": row['route_id'], "rsn": row.get('route_short_name'), "rln": row.get('route_long_name'), "rt": row.get('route_type')})
        session.commit()

        # 3. Calendar
        print("Importing calendar...")
        if os.path.exists(f"{extract_path}/calendar.txt"):
            cal_df = pd.read_csv(f"{extract_path}/calendar.txt")
            for _, row in cal_df.iterrows():
                # Fix for DatatypeMismatch: Convert YYYYMMDD to YYYY-MM-DD
                def format_date(d):
                    if pd.isna(d): return None
                    s = str(int(d))
                    if len(s) == 8:
                        return f"{s[:4]}-{s[4:6]}-{s[6:]}"
                    return s

                start_date = format_date(row['start_date'])
                end_date = format_date(row['end_date'])

                stmt = text("INSERT INTO calendar (service_id, start_date, end_date) VALUES (:sid, :sd, :ed) ON CONFLICT (service_id) DO NOTHING")
                session.execute(stmt, {"sid": row['service_id'], "sd": start_date, "ed": end_date})
            session.commit()

        # 4. Trips
        print("Importing trips...")
        trips_df = pd.read_csv(f"{extract_path}/trips.txt")
        for _, row in trips_df.iterrows():
            stmt = text("INSERT INTO trips (trip_id, route_id, service_id) VALUES (:tid, :rid, :sid) ON CONFLICT (trip_id) DO NOTHING")
            session.execute(stmt, {"tid": row['trip_id'], "rid": row['route_id'], "sid": row.get('service_id')})
        session.commit()

        # 5. Stop Times
        print("Importing stop times...")
        st_df = pd.read_csv(f"{extract_path}/stop_times.txt")
        for _, row in st_df.iterrows():
            stmt = text("INSERT INTO stop_times (trip_id, stop_id, arrival_time, departure_time, stop_sequence) VALUES (:tid, :sid, :at, :dt, :ss) ON CONFLICT DO NOTHING")
            session.execute(stmt, {"tid": row['trip_id'], "sid": row['stop_id'], "at": row.get('arrival_time'), "dt": row.get('departure_time'), "ss": row['stop_sequence']})
        session.commit()

        print("Import successful!")

    except Exception as e:
        print(f"Error during import: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to GTFS zip file")
    args = parser.parse_args()
    import_gtfs(args.file)
