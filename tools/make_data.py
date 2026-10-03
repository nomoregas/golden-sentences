"""Regenerate data/sentences.json from tools/sentences_src.py and validate it.

    python3 tools/make_data.py            # write data/sentences.json
    python3 tools/make_data.py --review   # also print every generated version for proofreading

Each template is filled in for every object in NOUNS. The masculine (Apfel)
version is stored as the sentence itself; feminine and neuter versions go in
"alt" with only the fields that differ.
"""
import json
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root / "tools"))
from sentences_src import FORMS, NOUNS, S, SETS  # noqa: E402

topics = json.loads((root / "data/topics.json").read_text(encoding="utf-8"))
CASES = {"N", "A", "D", "G", "v", "-"}
FIELDS = ["KF", "VF", "LK", "MF", "RK", "NF"]
GENDERS = list(NOUNS)  # m, f, n
PLACEHOLDER = re.compile(r"\{([^{}]+)\}")
errors, out, seen = [], [], set()


def fill(text, g, key):
    """Replace {placeholders} with the form for gender g."""
    if text is None:
        return None
    def sub(m):
        name = m.group(1)
        if name not in FORMS:
            errors.append(f"{key}: unknown placeholder {{{name}}}")
            return m.group(0)
        return FORMS[name][GENDERS.index(g)]
    return PLACEHOLDER.sub(sub, text)


def build(x, g):
    k = x["key"]
    toks = []
    for raw in x["toks"].split():
        parts = raw.split(":")
        if len(parts) != 4:
            errors.append(f"{k}: bad token {raw!r}")
            continue
        w, gl, c, f = parts
        if c not in CASES:
            errors.append(f"{k}: bad case {c!r} on {w}")
        if f not in FIELDS:
            errors.append(f"{k}: bad field {f!r} on {w}")
        toks.append({"w": fill(w, g, k), "g": fill(gl, g, k).replace("_", " "), "c": c, "f": f})
    de = fill(x["de"], g, k)
    m = re.match(r"^(.*?)([.?!])$", de)
    body = m.group(1) if m else de
    if " ".join(t["w"] for t in toks) != body:
        errors.append(f"{k}/{g}: tokens don't rebuild the sentence:\n  {' '.join(t['w'] for t in toks)}\n  {body}")
    order = [FIELDS.index(t["f"]) for t in toks if t["f"] in FIELDS]
    if order != sorted(order):
        errors.append(f"{k}: fields out of order")
    mistake = x["mistake"] and {"wrong": fill(x["mistake"]["wrong"], g, k), "why": fill(x["mistake"]["why"], g, k)}
    return {"en": fill(x["en"], g, k), "de": de, "tokens": toks, "note": fill(x["note"], g, k),
            "hint": fill(x["hint"], g, k), **({"mistake": mistake} if mistake else {})}


for i, x in enumerate(S, 1):
    k = x["key"]
    if k in seen:
        errors.append(f"{k}: duplicate key")
    seen.add(k)
    for t in x["topics"]:
        if t not in topics:
            errors.append(f"{k}: unknown topic {t!r}")
    if x["set"] not in SETS:
        errors.append(f"{k}: unknown set {x['set']!r}")
    versions = {g: build(x, g) for g in GENDERS}
    base = versions["m"]
    rec = {"id": i, "key": k, "set": x["set"], "source": x["source"], **base, "topics": x["topics"]}
    alt = {}
    for g in GENDERS[1:]:
        diff = {f: v for f, v in versions[g].items() if v != base.get(f)}
        if diff:
            alt[g] = diff
    if alt:
        rec["alt"] = alt
    out.append(rec)

unused = set(topics) - {t for x in S for t in x["topics"]}
if unused:
    errors.append(f"topics never referenced: {sorted(unused)}")
if errors:
    print("\n".join(errors))
    sys.exit(1)

(root / "data/sentences.json").write_text(
    json.dumps({"sets": SETS, "nouns": NOUNS, "sentences": out}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
counts = {s: sum(1 for x in out if x["set"] == s) for s in SETS}
swaps = sum(1 for x in out if "alt" in x)
print(f"{len(out)} sentences {counts}, {swaps} change with the object, {len(topics)} topics")

if "--review" in sys.argv:
    for x in out:
        print(f"\n{x['id']:>2} {x['key']}")
        print(f"   m  {x['de']}")
        for g in GENDERS[1:]:
            a = x.get("alt", {}).get(g, {})
            print(f"   {g}  {a.get('de', x['de'])}" + ("" if "de" in a else "   (same)"))
