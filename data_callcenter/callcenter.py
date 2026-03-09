import os
import csv
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

INPUT_FILE = os.path.join(os.path.dirname(__file__), "callcenter.csv")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "callcenter_result.csv")

SYSTEM_PROMPT = """You analyze call center transcripts. Extract these fields:
- CustomerName
- CustomerIntent
- CustomerRequest
- OurOffering
- Resolution

Each value MUST be under 30 characters. Be very concise."""

RESPONSE_FORMAT = {
    "type": "json_schema",
    "json_schema": {
        "name": "call_analysis",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "CustomerName":    {"type": "string"},
                "CustomerIntent":  {"type": "string"},
                "CustomerRequest": {"type": "string"},
                "OurOffering":     {"type": "string"},
                "Resolution":      {"type": "string"},
            },
            "required": [
                "CustomerName", "CustomerIntent", "CustomerRequest",
                "OurOffering", "Resolution",
            ],
            "additionalProperties": False,
        },
    },
}

def analyze(text):
    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        temperature=0,
        response_format=RESPONSE_FORMAT,
    )
    return json.loads(resp.choices[0].message.content)

def main():
    with open(INPUT_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    results = []
    for row in rows:
        print(f"Processing {row['RecordID']}...")
        extracted = analyze(row["TextScript"])
        results.append({
            "RecordID": row["RecordID"],
            "CustomerID": row["CustomerID"],
            "AgentName": row["AgentName"],
            "CustomerName": extracted["CustomerName"],
            "CustomerIntent": extracted["CustomerIntent"],
            "CustomerRequest": extracted["CustomerRequest"],
            "OurOffering": extracted["OurOffering"],
            "Resolution": extracted["Resolution"],
        })

    fieldnames = [
        "RecordID", "CustomerID", "AgentName",
        "CustomerName", "CustomerIntent", "CustomerRequest",
        "OurOffering", "Resolution",
    ]
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Saved {len(results)} rows to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
