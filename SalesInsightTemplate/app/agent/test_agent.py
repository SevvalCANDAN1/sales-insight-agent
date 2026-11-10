
import json
import re
import uuid
from urllib.request import Request, urlopen


url = "http://localhost:8080/invocations"
session_id = str(uuid.uuid4())

payload = {
    "prompt": "Satışları nasıl karşılaştırıyorsun?",
    "actorId": "sales-user"
}

request = Request(
    url,
    data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
    headers={
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "text/event-stream",
        "X-Amzn-Bedrock-AgentCore-Runtime-Session-Id": session_id,
    },
    method="POST"
)

response_text = ""

try:
    with urlopen(request) as response:
        for raw_line in response:
            line = raw_line.decode("utf-8").strip()

            if not line.startswith("data: "):
                continue

            event_data = json.loads(line[6:])
            event = event_data.get("event", {})

            delta = event.get("contentBlockDelta", {}).get("delta", {})
            response_text += delta.get("text", "")

    # Modelin düşünme bloğunu kullanıcıya göstermeyelim.
    response_text = re.sub(
        r"<thinking>.*?</thinking>",
        "",
        response_text,
        flags=re.DOTALL
    ).strip()

    print("\n--- SALES INSIGHT AGENT ---\n")
    print(response_text)

except Exception as error:
    print(f"Request failed: {error}")
