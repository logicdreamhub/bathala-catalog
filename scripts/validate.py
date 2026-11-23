"""Validate catalog.json before it reaches users' phones.

Run locally:  python3 scripts/validate.py
Pass the previous revision to also check it was bumped:  python3 scripts/validate.py --min-revision 3
"""
import json
import re
import sys

SUPPORTED_SCHEMA = 1
TIERS = {"lite", "standard", "smart"}
errors = []


def err(msg):
    errors.append(msg)


try:
    doc = json.load(open("catalog.json", encoding="utf-8"))
except Exception as e:  # noqa: BLE001
    sys.exit(f"catalog.json is not valid JSON: {e}")

if doc.get("schemaVersion") != SUPPORTED_SCHEMA:
    err(f"schemaVersion must be {SUPPORTED_SCHEMA}")
if not isinstance(doc.get("revision"), int):
    err("revision must be a whole number")

if "--min-revision" in sys.argv:
    prev = int(sys.argv[sys.argv.index("--min-revision") + 1])
    if isinstance(doc.get("revision"), int) and doc["revision"] <= prev:
        err(f"revision must be increased (was {prev}, now {doc['revision']}) or phones won't update")

cats = {c["id"] for c in doc.get("categories", [])}
models = {}
for m in doc.get("models", []):
    mid = m.get("id", "?")
    if mid in models:
        err(f"duplicate model id: {mid}")
    models[mid] = m
    if not re.match(r"^https://.+\.gguf(\?.*)?$", m.get("url", "")):
        err(f"model {mid}: url must be https and end with .gguf")
    if m.get("tier") not in TIERS:
        err(f"model {mid}: tier must be one of {sorted(TIERS)}")
    for k in ("sizeBytes", "minRamGB"):
        if not isinstance(m.get(k), (int, float)):
            err(f"model {mid}: {k} is required")
    if m.get("sha256") and not re.fullmatch(r"[0-9a-f]{64}", m["sha256"]):
        err(f"model {mid}: sha256 must be 64 lowercase hex characters")

seen = set()
for p in doc.get("presets", []):
    pid = p.get("id", "?")
    if pid in seen:
        err(f"duplicate preset id: {pid}")
    seen.add(pid)
    for k in ("title", "description", "categoryId"):
        if not p.get(k):
            err(f"preset {pid}: {k} is required")
    if not isinstance(p.get("systemPrompt"), str):
        err(f"preset {pid}: systemPrompt is required (use \"\" for the model's built-in prompt)")
    if p.get("categoryId") not in cats:
        err(f"preset {pid}: unknown categoryId '{p.get('categoryId')}'")
    ids = p.get("modelIds") or []
    if not ids:
        err(f"preset {pid}: modelIds must list at least one model")
    for i in ids:
        if i not in models:
            err(f"preset {pid}: unknown model '{i}'")

if errors:
    print("❌ catalog.json has problems:\n  - " + "\n  - ".join(errors))
    sys.exit(1)
print(f"✅ catalog.json OK — revision {doc['revision']}, {len(doc['presets'])} presets, {len(models)} models")
