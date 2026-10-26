def time_to_minutes(time_str: str) -> int:
    """Converts GTFS time string (HH:MM:SS) to minutes from midnight."""
    if not time_str:
        return 0
    parts = time_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    # Handle times > 24h (GTFS allows this for trips crossing midnight)
    return hours * 60 + minutes

def minutes_to_time(minutes: int) -> str:
    """Converts minutes from midnight back to HH:MM string."""
    hours = (minutes // 60) % 24
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"
