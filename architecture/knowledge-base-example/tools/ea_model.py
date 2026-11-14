"""Shared loaders.

  load_bb(root)    building blocks from LikeC4 (`likec4 export json model/bb`), normalised
  load_model(root) Markdown files under model/ (requirement details, dd, adr, notes, arb)
  gap(bb, a, b)    change of every ABB / SBB between two plateaus

Plateau membership is made of relationships (never tags), so parallel changes do not edit the same lines:
  - the first plateau of an application aggregates what exists (`imp.<app>.baseline -[aggregation]-> x`);
  - each next plateau (order: the `triggering` chain between plateaus) = the previous one
    + what the work packages realizing it realize (and any explicit aggregation) − what they `'retires'`.
New / changed / retired are derived: new = absent from the first plateau and present in the last; retired = the
opposite; changed = in both and realized by a work package.
"""
from __future__ import annotations
import json, os, re, shlex, subprocess, sys, tempfile
from pathlib import Path
import yaml

FM_RE = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.S)
LIKEC4 = shlex.split(os.environ.get("LIKEC4", "npx -y likec4@1.41.0"))

FOLDER_LEVEL = {"mot": "motivation", "req": "requirement", "abb": "abb", "sbb": "sbb", "imp": "migration"}
PLATEAUS = ["baseline", "transition-1", "transition-2", "target"]
CHANGES = ["new", "changed", "retired"]
STATUSES = ["draft", "ready", "done", "deprecated"]
APP_LAYER_SBB = {"application-component", "application-interface", "application-collaboration", "application-function",
                 "application-interaction", "application-process", "application-event", "application-service", "data-object"}
TECH_KINDS = {"node", "device", "system-software", "technology-collaboration", "technology-interface", "path",
              "communication-network", "technology-function", "technology-process", "technology-interaction",
              "technology-event", "technology-service", "artifact"}


def export_bb(root: Path) -> dict:
    """Run `likec4 export json` on model/bb and return the raw model."""
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "bb.json"
        r = subprocess.run(LIKEC4 + ["export", "json", "-o", str(out), str(root / "model" / "bb")], capture_output=True, text=True)
        if r.returncode != 0 or not out.exists():
            sys.stderr.write(r.stdout[-3000:] + r.stderr[-3000:])
            raise SystemExit("likec4 export failed: run `likec4 validate model/bb` for details")
        return json.loads(out.read_text(encoding="utf-8"))


def _meta(v):
    return v if isinstance(v, str) else (", ".join(v) if isinstance(v, list) else str(v))


def load_bb(root: Path, raw: dict | None = None) -> dict:
    raw = raw or export_bb(root)
    elements, groups = {}, {}
    for fqn, e in raw["elements"].items():
        parts = fqn.split(".")
        if e["kind"] == "grouping":
            groups[fqn] = e.get("title", fqn)
            continue
        tags = e.get("tags") or []
        md = {k: _meta(v) for k, v in (e.get("metadata") or {}).items()}
        desc = e.get("description")
        if isinstance(desc, dict):
            desc = desc.get("txt") or desc.get("md") or ""
        elements[fqn] = {
            "id": fqn, "level": FOLDER_LEVEL.get(parts[0], "other"), "kind": e["kind"], "title": e.get("title", fqn),
            "application": parts[1] if len(parts) > 2 else None,
            "description": desc or "", "tags": tags,
            "plateaus": [], "change": None,
            "status": next((t for t in STATUSES if t in tags), None),
            "metadata": md, "owner": md.get("owner"), "module": md.get("module"), "workItemId": md.get("workItemId"),
            "contract": md.get("contract"), "adr": [a.strip() for a in md.get("adr", "").split(",") if a.strip()],
            "domainRef": md.get("domainRef"),
            "in": [], "out": [],
        }
    relations = []
    for rid, r in raw["relations"].items():
        s, t = r["source"]["model"], r["target"]["model"]
        rel = {"id": rid, "source": s, "target": t, "kind": r.get("kind") or "association", "title": r.get("title") or ""}
        relations.append(rel)
        if s in elements:
            elements[s]["out"].append(rel)
        if t in elements:
            elements[t]["in"].append(rel)
    order = _plateau_membership(elements, relations)
    return {"elements": elements, "relations": relations, "groups": groups, "plateauOrder": order,
            "views": {k: {"title": v.get("title") or k} for k, v in raw.get("views", {}).items()}}


def _is_retire(r: dict) -> bool:
    return r["kind"] == "association" and r["title"].strip().lower() == "retires"


def _plateau_membership(elements: dict, relations: list) -> dict[str, list[str]]:
    """Fill e["plateaus"] and e["change"] from relationships. Returns {application: [plateau short names in order]}."""
    def rank(fqn):
        n = fqn.split(".")[-1]
        return PLATEAUS.index(n) if n in PLATEAUS else 99
    by_app: dict[str, list[str]] = {}
    for fqn, e in elements.items():
        if e["kind"] == "plateau":
            by_app.setdefault(e["application"], []).append(fqn)
    orders = {}
    for app, ids in by_app.items():
        nxt = {r["source"]: r["target"] for r in relations
               if r["kind"] == "triggering" and r["source"] in ids and r["target"] in ids}
        starts = sorted([i for i in ids if i not in nxt.values()], key=rank)
        order, cur = [], (starts or sorted(ids, key=rank))[0]
        while cur and cur not in order:
            order.append(cur)
            cur = nxt.get(cur)
        order += sorted((i for i in ids if i not in order), key=rank)
        members: set[str] = set()
        for pid in order:
            wps = {r["source"] for r in relations if r["kind"] == "realization" and r["target"] == pid
                   and elements.get(r["source"], {}).get("kind") == "work-package"}
            adds = {r["target"] for r in relations if r["source"] == pid and r["kind"] == "aggregation"}
            adds |= {r["target"] for r in relations if r["source"] in wps and r["kind"] == "realization"
                     and elements.get(r["target"], {}).get("level") in ("abb", "sbb")}
            rets = {r["target"] for r in relations if r["source"] in wps | {pid} and _is_retire(r)}
            members = (members | adds) - rets
            for m in sorted(members):
                if m in elements:
                    elements[m]["plateaus"].append(pid.split(".")[-1])
        first, last = order[0].split(".")[-1], order[-1].split(".")[-1]
        for e in elements.values():
            if e["application"] != app or e["level"] not in ("abb", "sbb") or not e["plateaus"]:
                continue
            a, b = first in e["plateaus"], last in e["plateaus"]
            if b and not a:
                e["change"] = "new"
            elif not b:
                e["change"] = "retired"
            elif any(elements.get(r["source"], {}).get("kind") == "work-package" and r["kind"] == "realization" for r in e["in"]):
                e["change"] = "changed"
        orders[app] = [o.split(".")[-1] for o in order]
    return orders


def load_model(root: Path) -> tuple[dict[str, dict], list[str]]:
    """Markdown files under model/ (bb/ excluded). Returns ({id: {fm, body, path}}, errors)."""
    elements: dict[str, dict] = {}
    errors: list[str] = []
    for path in sorted((root / "model").rglob("*.md")):
        if "bb" in path.relative_to(root / "model").parts[:1]:
            continue
        rel = path.relative_to(root)
        m = FM_RE.match(path.read_text(encoding="utf-8"))
        if not m:
            errors.append(f"{rel}: no frontmatter block"); continue
        try:
            fm = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError as e:
            errors.append(f"{rel}: YAML error: {e}"); continue
        for k in ("updatedAt", "start", "end", "boardDate", "submittedAt"):
            if k in fm and not isinstance(fm[k], str):
                fm[k] = fm[k].isoformat()
        for rv in fm.get("reviewers") or []:
            if "at" in rv and not isinstance(rv["at"], str):
                rv["at"] = rv["at"].isoformat()
        for c in fm.get("conditions") or []:
            if "due" in c and not isinstance(c["due"], str):
                c["due"] = c["due"].isoformat()
        eid = fm.get("id")
        if not eid:
            errors.append(f"{rel}: missing id"); continue
        if eid in elements:
            errors.append(f"{rel}: duplicate id {eid} (also in {elements[eid]['path'].relative_to(root)})"); continue
        if path.stem != eid:
            errors.append(f"{rel}: file name must equal id ({eid})")
        elements[eid] = {"fm": fm, "body": m.group(2), "path": path}
    return elements, errors


def gap(bb: dict, a: str, b: str) -> list[dict]:
    """Change of each ABB / SBB from plateau tag a to plateau tag b."""
    out = []
    for e in bb["elements"].values():
        if e["level"] not in ("abb", "sbb"):
            continue
        ina, inb = a in e["plateaus"], b in e["plateaus"]
        if not ina and not inb:
            continue
        if ina and not inb:
            ch = "retired"
        elif inb and not ina:
            ch = "new"
        else:
            wps = [r for r in e["in"] if r["kind"] == "realization" and bb["elements"].get(r["source"], {}).get("kind") == "work-package"
                   and any(x["kind"] == "realization" and x["target"].split(".")[-1] in _between(bb, e["application"], a, b)
                           for x in bb["elements"][r["source"]]["out"])]
            ch = "changed" if wps else "unchanged"
        out.append({"id": e["id"], "change": ch})
    return out


def _between(bb: dict, app: str, a: str, b: str) -> list[str]:
    """Plateaus after a, up to and including b."""
    order = bb.get("plateauOrder", {}).get(app) or PLATEAUS
    if a in order and b in order:
        return order[order.index(a) + 1: order.index(b) + 1]
    return [b]


def addressed_by(bb: dict, eid: str) -> list[str]:
    """Work packages that realise (or retire) an element."""
    return sorted({r["source"] for r in bb["elements"][eid]["in"]
                   if bb["elements"].get(r["source"], {}).get("kind") == "work-package"})
