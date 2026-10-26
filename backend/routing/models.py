from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Stop:
    stop_id: str
    name: str
    lat: float
    lon: float

@dataclass
class StopTime:
    trip_id: str
    arrival_time: int # Minutes from midnight
    departure_time: int # Minutes from midnight
    stop_sequence: int

@dataclass
class Trip:
    trip_id: str
    route_id: str
    service_id: str

@dataclass
class Route:
    route_id: str
    short_name: str
    long_name: str
    route_type: int

@dataclass
class PathNode:
    stop_id: str
    arrival_time: int
    trip_id: str
    prev_node: Optional['PathNode'] = None
