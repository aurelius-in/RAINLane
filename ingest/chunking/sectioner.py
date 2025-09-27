import re
from typing import Dict, List


def to_sections(raw_doc: Dict) -> List[Dict]:
    txt = raw_doc.get("raw", "")
    if not txt:
        return []
    # naive: split by double newline or headings like "\n\d+.\d+ "
    parts = re.split(r"\n\n+|\n(?=\d+\.\d+\s)", txt)
    sections = []
    for idx, part in enumerate(parts, start=1):
        part = part.strip()
        if not part:
            continue
        title = part.split("\n", 1)[0][:80]
        sections.append({"id": f"sec-{idx}", "title": title, "text": part})
    return sections


