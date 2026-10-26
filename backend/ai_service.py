import os
import json
from typing import Optional
from anthropic import Anthropic
from ai_schemas import AIJourneyRequest, AIChatRequest
from ai_crud import resolve_stop_name
from sqlalchemy.orm import Session

# Load API key from environment
api_key = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(api_key=api_key) if api_key else None

def extract_journey_params(user_text: str) -> AIJourneyRequest:
    if not client:
        raise RuntimeError("Anthropic API key not configured")

    prompt = (
        "Extract journey details from the following user request into a JSON object. "
        "Fields: origin, destination, time, optimization (fastest/fewest_transfers), max_transfers. "
        "If a field is missing, use null or a reasonable default. "
        "Return ONLY the JSON object. No preamble."
    )

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        temperature=0,
        system="You are a transit assistant that extracts structured journey data. "
              "You must return valid JSON. "
              "If the request is not about travel or is impossible (e.g., 'Go to Mars'), "
              "return a JSON object with 'error': 'invalid_request' and a 'message'."
              "Do not invent locations.",
        messages=[{"role": "user", "content": f"{prompt}\n\nUser: {user_text}"}]
    )

    content = message.content[0].text
    try:
        data = json.loads(content)
        if "error" in data:
            raise ValueError(data["message"])
        return AIJourneyRequest(**data)
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError(f"AI failed to extract valid request: {str(e)}")

def process_ai_request(db: Session, user_text: str):
    # 1. Extract params
    try:
        params = extract_journey_params(user_text)
    except ValueError as e:
        return {"error": str(e), "status": "rejected"}

    # 2. Resolve Locations
    origin_res = resolve_stop_name(db, params.origin)
    dest_res = resolve_stop_name(db, params.destination)

    if not origin_res.found or not dest_res.found:
        missing = []
        if not origin_res.found: missing.append(f"origin '{params.origin}'")
        if not dest_res.found: missing.append(f"destination '{params.destination}'")
        return {
            "error": f"Could not find: {', '.join(missing)}",
            "status": "not_found"
        }

    if origin_res.ambiguous or dest_res.ambiguous:
        return {
            "error": "Ambiguous locations",
            "suggestions": {
                "origin": origin_res.suggestions if origin_res.ambiguous else None,
                "destination": dest_res.suggestions if dest_res.ambiguous else None
            },
            "status": "ambiguous"
        }

    # 3. Return validated parameters for the routing engine
    return {
        "origin_id": origin_res.stop_id,
        "destination_id": dest_res.stop_id,
        "time": params.time,
        "optimization": params.optimization,
        "max_transfers": params.max_transfers,
        "status": "validated"
    }

def explain_journey(user_query: str, journey_data: any) -> str:
    if not client:
        raise RuntimeError("Anthropic API key not configured")

    system_prompt = (
        "You are a friendly transit assistant for Chennai. "
        "Your task is to explain journey results to the user. "
        "Rules:\n"
        "1. Clearly label each leg as 'Scheduled' (if it follows GTFS timing) or 'Estimated' (if it is a walk/gap).\n"
        "2. Be concise but helpful.\n"
        "3. Mention total duration and arrival time.\n"
        "4. If no journey was found, explain why politely."
    )

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        temperature=0.7,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": f"User Query: {user_query}\n\nJourney Data: {json.dumps(journey_data)}"
        }]
    )

    return message.content[0].text
