"""Regenerate data/sentences.json from tools/sentences_src.py and validate it.

    python3 tools/make_data.py
"""
import json
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root / "tools"))
from sentences_src import S, SETS  # noqa: E402

topics = json.loads((root / "data/topics.json").read_text(encoding="utf-8"))
CASES = {"N", "A", "D", "G", "v", "-"}
FIELDS = ["KF", "VF", "LK", "MF", "RK", "NF"]
errors, out, seen = [], [], set()

for i, x in enumerate(S, 1):
    k = x["key"]
    if k in seen:
        errors.append(f"{k}: duplicate key")
    seen.add(k)
    toks = []
    for raw in x["toks"].split():
        parts = raw.split(":")
        if len(parts) != 4:
            errors.append(f"{k}: bad token {raw!r}")
            continue
        w, g, c, f = parts
        if c not in CASES:
            errors.append(f"{k}: bad case {c!r} on {w}")
        if f not in FIELDS:
            errors.append(f"{k}: bad field {f!r} on {w}")
        toks.append({"w": w, "g": g.replace("_", " "), "c": c, "f": f})
    m = re.match(r"^(.*?)([.?!])$", x["de"])
    body = m.group(1) if m else x["de"]
    if " ".join(t["w"] for t in toks) != body:
        errors.append(f"{k}: tokens don't rebuild the sentence:\n  {' '.join(t['w'] for t in toks)}\n  {body}")
    order = [FIELDS.index(t["f"]) for t in toks if t["f"] in FIELDS]
    if order != sorted(order):
        errors.append(f"{k}: fields out of order")
    for t in x["topics"]:
        if t not in topics:
            errors.append(f"{k}: unknown topic {t!r}")
    if x["set"] not in SETS:
        errors.append(f"{k}: unknown set {x['set']!r}")
    rec = {"id": i, "key": k, "set": x["set"], "source": x["source"], "en": x["en"], "de": x["de"],
           "tokens": toks, "topics": x["topics"], "note": x["note"], "hint": x["hint"]}
    if x["mistake"]:
        rec["mistake"] = x["mistake"]
    out.append(rec)

unused = set(topics) - {t for x in S for t in x["topics"]}
if unused:
    errors.append(f"topics never referenced: {sorted(unused)}")
if errors:
    print("\n".join(errors))
    sys.exit(1)

(root / "data/sentences.json").write_text(
    json.dumps({"sets": SETS, "sentences": out}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
counts = {s: sum(1 for x in out if x["set"] == s) for s in SETS}
print(f"{len(out)} sentences {counts}, {len(topics)} topics, {sum('mistake' in x for x in out)} with a common mistake")
