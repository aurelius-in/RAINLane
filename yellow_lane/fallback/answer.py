def answer_yellow(query: str, docs: dict):
    return f"Advisory: Refer to SOP index for '{query}'.", [
        {"doc_id": "index", "section": "1", "span": [0, 10]}
    ]


