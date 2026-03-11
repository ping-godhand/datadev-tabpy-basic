import os
import json
import pandas as pd
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

INPUT_FILE = "data/04-Callcenter.csv"

SYSTEM_PROMPT = """You analyze call center transcripts. Extract these fields:
- CustomerName
- CustomerIntent
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
                "Resolution":      {"type": "string"},
            },
            "required": [
                "CustomerName", "CustomerIntent", "Resolution",
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
    df = pd.read_csv(INPUT_FILE)

    results = []
    for _, row in df.iterrows():
        print(f"Processing {row['RecordID']}...")
        extracted = analyze(row["TextScript"])
        results.append({
            "RecordID": row["RecordID"],
            "CustomerID": row["CustomerID"],
            "CustomerName": extracted["CustomerName"],
            "CustomerIntent": extracted["CustomerIntent"],
            "Resolution": extracted["Resolution"],
        })

    result_df = pd.DataFrame(results)
    print(result_df.to_string(index=False))
    print(f"\n({len(result_df)} rows)")

if __name__ == "__main__":
    main()
