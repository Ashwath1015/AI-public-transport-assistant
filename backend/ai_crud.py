from sqlalchemy.orm import Session
from sqlalchemy import text
from ai_schemas import AIResolutionResponse

def resolve_stop_name(db: Session, stop_name: str) -> AIResolutionResponse:
    # Simple fuzzy search for the demo, using ILIKE
    # In a production app, this would use pg_trgm or similar
    query = text("SELECT stop_id, stop_name FROM stops WHERE stop_name ILIKE :name ORDER by stop_name ASC")
    result = db.execute(query, {"name": f"%{stop_name}%"}).fetchall()

    if not result:
        return AIResolutionResponse(found=False, stop_id=None, ambiguous=False, suggestions=[])

    if len(result) > 1:
        return AIResolutionResponse(
            found=True,
            stop_id=None,
            ambiguous=True,
            suggestions=[r[1] for r in result]
        )

    return AIResolutionResponse(
        found=True,
        stop_id=result[0][0],
        ambiguous=False,
        suggestions=[result[0][1]]
    )
