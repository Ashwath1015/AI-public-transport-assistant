from sqlalchemy.orm import Session
from sqlalchemy import text
from routing.engine import RaptorEngine
from schemas import JourneyRequest, JourneyResponse, JourneyLeg, StopResponse
from routing.utils import minutes_to_time

def search_stops(db: Session, q: str = None, lat: float = None, lon: float = None, radius: int = 500, limit: int = 10):
    if q:
        # Simple name search
        query = text("SELECT stop_id, stop_name, stop_lat, stop_lon FROM stops WHERE stop_name ILIKE :q LIMIT :limit")
        result = db.execute(query, {"q": f"%{q}%", "limit": limit})
    elif lat and lon:
        # Spatial search using PostGIS
        query = text("SELECT stop_id, stop_name, stop_lat, stop_lon FROM stops WHERE ST_DWithin(geom, ST_MakePoint(:lon, :lat)::geography, :radius) LIMIT :limit")
        result = db.execute(query, {"lon": lon, "lat": lat, "radius": radius, "limit": limit})
    else:
        return []

    return [StopResponse(stop_id=r[0], stop_name=r[1], stop_lat=r[2], stop_lon=r[3]) for r in result]

def search_journeys(db: Session, req: JourneyRequest):
    origin_id = req.origin_id

    # Safety Net: If the frontend sends the mock ID 'S1', resolve it to the real Anna Nagar ID
    if origin_id == "S1":
        res = db.execute(text("SELECT stop_id FROM stops WHERE stop_name ILIKE '%Anna Nagar%' LIMIT 1")).fetchone()
        if res:
            origin_id = res[0]
            print(f"DEBUG: Translated mock ID 'S1' to real ID '{origin_id}'")

    print(f"DEBUG: Searching Journey - Origin: {origin_id}, Destination: {req.destination_id}, Time: {req.departure_time}")
    engine = RaptorEngine(db)
    result = engine.search_dijkstra(origin_id, req.destination_id, req.departure_time)

    if not result or len(result) < 3:
        print(f"DEBUG: No path found for {origin_id} -> {req.destination_id}")
        return None

    arrival_time, path, trip_ids = result

    legs = []
    # Fetch all stop info needed for this journey to avoid N+1 queries
    stop_ids = path
    stops_info = {
        row[0]: {"name": row[1], "lat": row[2], "lon": row[3]}
        for row in db.execute(
            text("SELECT stop_id, stop_name, stop_lat, stop_lon FROM stops WHERE stop_id IN :ids"),
            {"ids": tuple(stop_ids)}
        ).fetchall()
    }

    for i in range(len(path) - 1):
        from_stop = path[i]
        to_stop = path[i+1]
        trip_id = trip_ids[i]
        route_id = engine.trips[trip_id].route_id

        dep_time = "N/A"
        arr_time = "N/A"
        for st in engine.stop_times[from_stop]:
            if st.trip_id == trip_id:
                dep_time = minutes_to_time(st.departure_time)
                break
        for st in engine.stop_times[to_stop]:
            if st.trip_id == trip_id:
                arr_time = minutes_to_time(st.arrival_time)
                break

        # Get info from our map
        from_info = stops_info.get(from_stop, {"name": from_stop, "lat": 0.0, "lon": 0.0})
        to_info = stops_info.get(to_stop, {"name": to_stop, "lat": 0.0, "lon": 0.0})

        legs.append(JourneyLeg(
            trip_id=trip_id,
            route_id=route_id,
            from_stop=from_stop,
            from_stop_name=from_info["name"],
            to_stop=to_stop,
            to_stop_name=to_info["name"],
            from_lat=from_info["lat"],
            from_lon=from_info["lon"],
            to_lat=to_info["lat"],
            to_lon=to_info["lon"],
            dep_time=dep_time,
            arr_time=arr_time
        ))

    return JourneyResponse(
        total_duration=arrival_time - req.departure_time,
        arrival_time=minutes_to_time(arrival_time),
        legs=legs
    )
