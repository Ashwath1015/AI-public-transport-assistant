import json
from anthropic import Anthropic
import os

# Mocking the DB for a quick logic check
def mock_resolve_stop_name(stop_name):
    db_stops = {
        "Chennai Central": "S1",
        "T Nagar": "S2",
        "T Nagar Bus Terminus": "S3"
    }
    matches = [id for name, id in db_stops.items() if stop_name.lower() in name.lower()]

    if not matches:
        return {"found": False, "stop_id": None, "ambiguous": False, "suggestions": []}
    if len(matches) > 1:
        return {"found": True, "stop_id": None, "ambiguous": True, "suggestions": [n for n, i in db_stops.items() if i in matches]}

    name = [n for n, id in db_stops.items() if id == matches[0]][0]
    return {"found": True, "stop_id": matches[0], "ambiguous": False, "suggestions": [name]}

def test_ai_logic():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Skipping AI call: No API key found.")
        return

    client = Anthropic(api_key=api_key)

    test_cases = [
        "Go from Chennai Central to T Nagar",
        "I want to go to T Nagar",
        "Take me to Mars"
    ]

    for text in test_cases:
        print(f"\nTesting: {text}")
        # Mocking the extract_journey_params call
        prompt = "Extract origin, destination, time, optimization, max_transfers as JSON. If impossible, return {'error': 'invalid_request'}"
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            temperature=0,
            messages=[{"role": "user", "content": f"{prompt}\n\nUser: {text}"}]
        )

        try:
            res = json.loads(message.content[0].text)
            print(f"AI Extracted: {res}")

            if "error" in res:
                print("Result: Rejected as expected for invalid requests.")
                continue

            origin = res.get("origin", "")
            dest = res.get("destination", "")

            o_res = mock_resolve_stop_name(origin)
            d_res = mock_resolve_stop_name(dest)

            print(f"Origin Resolve: {o_res}")
            print(f"Dest Resolve: {d_res}")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_ai_logic()
