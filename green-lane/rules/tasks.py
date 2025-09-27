def detect_task(query: str) -> str:
    q = query.lower()
    if "table" in q:
        return "table_lookup"
    if any(x in q for x in ["unit", "calculate", "ratio"]):
        return "math_units"
    return "extractive"


