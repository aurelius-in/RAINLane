import json
import os
import requests

CASES = [
    {"q": "what is the sterile changeover checklist?", "role": "Operator", "expect_lane": "green"},
    {"q": "where is the gowning table?", "role": "Visitor", "expect_lane": "yellow"},
]


def main():
    metrics = []
    for c in CASES:
        r = requests.post(
            "http://localhost:8000/v1/answer",
            json={"query": c["q"], "user_role": c["role"]},
        ).json()
        metrics.append({
            "q": c["q"],
            "lane": r["lane"],
            "latency_ms": r["metrics"]["latency_ms"],
        })
    os.makedirs("evals/reports", exist_ok=True)
    with open("evals/reports/metrics.json", "w") as f:
        json.dump({"results": metrics}, f, indent=2)


if __name__ == "__main__":
    main()


