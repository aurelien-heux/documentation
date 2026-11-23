#!/usr/bin/env python3
"""Validate the architecture knowledge base and compute ARB readiness.

  1. building blocks: `likec4 export json model/bb` (LikeC4 must validate first)
  2. Markdown: schema per file + required keys per level
  3. checks across both, grouped as in the ARB checklist (see CHECKS below)
  4. ARB readiness for every submission in model/arb/

Writes dist/bb.json (normalised building blocks) and dist/validation.json.
Exit 1 when an error-level check fails (blocks the PR); warnings are reported to the ARB, not blocking.

Usage: python3 tools/validate.py [root]          Env: LIKEC4=/path/to/likec4
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
from jsonschema import Draft202012Validator

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ea_model import load_bb, load_model, export_bb, gap, addressed_by, APP_LAYER_SBB, TECH_KINDS, PLATEAUS  # noqa: E402

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else Path(__file__).resolve().parents[1]

# id, group, title, severity (error blocks the PR; warning is shown to the ARB)
CHECKS = [
    ("S1", "Structure",            "Markdown frontmatter matches the schema",                          "error"),
    ("S2", "Structure",            "Every Markdown reference resolves to a building block or a file",  "error"),
    ("S3", "Structure",            "Detailed design realizes Solution Building Blocks only",           "error"),
    ("T1", "Traceability",         "Every new or changed ABB realizes a requirement",                  "error"),
    ("T2", "Traceability",         "Every new or changed application SBB realizes an ABB",             "error"),
    ("T3", "Traceability",         "Every new or changed technology SBB serves another SBB",           "warning"),
    ("T4", "Traceability",         "Every requirement is realized by at least one ABB",                "error"),
    ("T5", "Traceability",         "Every requirement has acceptance criteria and operational figures","error"),
    ("T6", "Traceability",         "Every new or changed application SBB has a detailed design",       "warning"),
    ("P1", "Plateaus & gaps",      "Every ABB and SBB belongs to at least one plateau",                "error"),
    ("P2", "Plateaus & gaps",      "Plateau membership and change are relationships, not tags",        "error"),
    ("P3", "Plateaus & gaps",      "Every gap item is addressed by a work package",                    "warning"),
    ("P4", "Plateaus & gaps",      "Plateaus are chained from baseline to target",                     "warning"),
    ("P5", "Plateaus & gaps",      "No building block uses a block retired by another change",       "error"),
    ("O1", "Ownership & contracts","Every new or changed building block has an owner",                 "error"),
    ("O2", "Ownership & contracts","Interfaces and events reference a contract file that exists",      "error"),
    ("O3", "Ownership & contracts","New or changed SBB and ready DD carry a Work item",                         "error"),
    ("D1", "Decisions",            "Every referenced ADR exists",                                       "error"),
    ("D2", "Decisions",            "Every new application component is covered by an ADR",              "warning"),
    ("D3", "Decisions",            "Accepted ADRs name their domain-reference entry",                   "error"),
    ("C1", "Parallel changes",     "Each change file declares one work package named after the file",  "error"),
    ("C2", "Parallel changes",     "No building block is retired twice or changed after it is retired","error"),
    ("C3", "Parallel changes",     "Dependencies between changes exist, have no cycle, follow plateau order", "error"),
    ("C4", "Parallel changes",     "Blocks touched by two changes have a declared dependency between them", "warning"),
]
OLD_TAGS = {"baseline", "transition-1", "transition-2", "target", "new", "changed", "retired"}
STRUCTURAL = {"serving", "access", "composition", "aggregation", "assignment", "realization", "flow", "triggering"}


def run(root: Path) -> tuple[dict, dict, dict]:
    schema = json.loads((root / "ea-schema.json").read_text(encoding="utf-8"))
    level_requires = schema["$defs"]["levelRequires"]
    raw = export_bb(root)
    bb = load_bb(root, raw)
    E = bb["elements"]
    md, load_errors = load_model(root)
    findings = {c[0]: [] for c in CHECKS}

    def f(check, eid, msg):
        findings[check].append({"id": eid, "message": msg})

    for e in load_errors:
        f("S1", None, e)

    # ---------- Markdown: schema, required keys, references ----------
    validator = Draft202012Validator(schema)
    for mid, m in md.items():
        fm = m["fm"]
        for err in sorted(validator.iter_errors(fm), key=str):
            f("S1", mid, err.message)
        lvl = fm.get("level")
        for key in level_requires.get(lvl, []):
            if key not in fm:
                f("S1", mid, f"{lvl} requires '{key}'")
        if lvl == "dd" and fm.get("kind") not in schema["$defs"]["ddKinds"]:
            f("S1", mid, f"DD kind '{fm.get('kind')}' unknown")
        if lvl in ("dd", "adr") and fm.get("status") not in schema["$defs"]["statuses"]:
            f("S1", mid, f"status '{fm.get('status')}' unknown")
        if lvl == "arb" and fm.get("status") not in schema["$defs"]["arbStatuses"]:
            f("S1", mid, f"ARB status '{fm.get('status')}' unknown")
        if lvl in ("requirement", "note") and mid not in E:
            f("S2", mid, f"{lvl} file for '{mid}', which is not a building block in model/bb")
        if lvl == "requirement" and mid in E and E[mid]["kind"] not in ("requirement", "constraint"):
            f("S2", mid, f"'{mid}' is a {E[mid]['kind']}, not a requirement")
        for ref in fm.get("realizes") or []:
            if ref not in E:
                f("S2", mid, f"realizes '{ref}', which is not in the LikeC4 model")
            elif lvl == "dd" and E[ref]["level"] != "sbb":
                f("S3", mid, f"realizes '{ref}' ({E[ref]['level'].upper()}); DD realizes SBB only")
        for ref in fm.get("dependsOn") or []:
            if ref not in md:
                f("S2", mid, f"dependsOn '{ref}' not found")
        for ref in fm.get("affects") or []:
            if ref not in E and ref not in md:
                f("S2", mid, f"affects '{ref}' not found")
        for ref in fm.get("adr") or []:
            if ref not in md:
                f("D1", mid, f"ADR '{ref}' not found in model/adr")
        for ref in fm.get("requirements") or []:
            if ref not in E:
                f("S2", mid, f"requirement '{ref}' not in the LikeC4 model")
        for k in ("from", "to"):
            if fm.get(k) and (fm[k] not in E or E[fm[k]]["kind"] != "plateau"):
                f("S2", mid, f"{k} '{fm[k]}' is not a plateau")
        if fm.get("contract") and not (root / fm["contract"]).is_file():
            f("O2", mid, f"contract '{fm['contract']}' not found")
        if lvl == "dd":
            if fm.get("module") and not str(fm["module"]).startswith(str(fm.get("application")) + "/"):
                f("S1", mid, f"module '{fm['module']}' must belong to application '{fm.get('application')}'")
            if fm.get("status") in ("ready", "done") and not fm.get("workItemId"):
                f("O3", mid, "ready DD without workItemId")
        if lvl == "adr" and fm.get("status") == "done" and not fm.get("domainRef"):
            f("D3", mid, "accepted ADR without domainRef")

    # ---------- Building blocks ----------
    dd_by_sbb = {}
    for mid, m in md.items():
        if m["fm"].get("level") == "dd":
            for ref in m["fm"].get("realizes") or []:
                dd_by_sbb.setdefault(ref, []).append(mid)

    def realizes(e, level_or_kinds):
        return [r["target"] for r in e["out"] if r["kind"] == "realization" and r["target"] in E
                and (E[r["target"]]["level"] == level_or_kinds or E[r["target"]]["kind"] in (level_or_kinds if isinstance(level_or_kinds, set) else ()))]

    for eid, e in E.items():
        changed = e["change"] in ("new", "changed")
        if e["level"] in ("abb", "sbb"):
            if not e["plateaus"]:
                f("P1", eid, "in no plateau: aggregate it from the baseline, or realize it from a work package")
            ch = e["change"]
            if ch in ("new", "changed"):
                # A relationship holds from the first plateau where both ends exist. It breaks when the target leaves a
                # later plateau the source is still in, unless the change that retires the target also changes the source.
                mine = {r["source"] for r in e["in"] if r["kind"] == "realization" and E.get(r["source"], {}).get("kind") == "work-package"}
                for r in e["out"]:
                    t = E.get(r["target"])
                    if r["kind"] not in STRUCTURAL or not t or t["level"] not in ("abb", "sbb") or not t["plateaus"]:
                        continue
                    both = [p for p in e["plateaus"] if p in t["plateaus"]]
                    if not both:
                        f("P5", eid, f"{r['kind']} → {r['target']}: the two never exist in the same plateau")
                        continue
                    retirers = {x["source"] for x in t["in"] if x["kind"] == "association" and x["title"].strip().lower() == "retires"}
                    if retirers & mine:
                        continue
                    after = e["plateaus"][e["plateaus"].index(both[0]):]
                    lost = [p for p in after if p not in t["plateaus"]]
                    if lost:
                        f("P5", eid, f"{r['kind']} → {r['target']}, which is retired in {lost[0]}"
                                     + (f" by {', '.join(sorted(retirers))}" if retirers else ""))
            if ch in ("new", "changed", "retired") and not addressed_by(bb, eid):
                f("P3", eid, f"{ch} but no work package realizes or retires it")
            if changed and not e["owner"]:
                f("O1", eid, "no owner metadata")
            if changed and e["status"] in ("ready", "done") and e["level"] == "sbb" and e["kind"] in APP_LAYER_SBB and not e["workItemId"]:
                f("O3", eid, f"{e['status']} SBB without workItemId")
        if e["level"] == "abb" and changed and not realizes(e, {"requirement", "constraint"}):
            f("T1", eid, "realizes no requirement")
        if e["level"] == "sbb" and changed:
            if e["kind"] in APP_LAYER_SBB and not realizes(e, "abb"):
                f("T2", eid, "realizes no ABB")
            if e["kind"] in TECH_KINDS:
                serves = [r for r in e["out"] if r["kind"] in ("serving", "assignment", "access", "realization") and E.get(r["target"], {}).get("level") == "sbb"]
                if not serves:
                    f("T3", eid, "serves, hosts or accesses no other SBB")
            if e["kind"] in APP_LAYER_SBB and not dd_by_sbb.get(eid):
                sev = "no detailed design yet" + (" (status draft)" if e["status"] == "draft" else "")
                f("T6", eid, sev)
            if e["kind"] == "application-component" and e["change"] == "new" and not e["adr"]:
                f("D2", eid, "new application component without an ADR")
        if e["kind"] in ("application-interface", "application-event") and e["level"] == "sbb" and e["change"] != "retired":
            if not e["contract"]:
                f("O2", eid, "no contract metadata")
            elif not (root / e["contract"]).is_file():
                f("O2", eid, f"contract '{e['contract']}' not found")
        old = sorted(t for t in e["tags"] if t in OLD_TAGS)
        if old:
            f("P2", eid, "remove tag(s) " + " ".join("#" + t for t in old) + ": plateaus come from relationships, the change is derived")
        for a in e["adr"]:
            if a not in md:
                f("D1", eid, f"ADR '{a}' not found in model/adr")
        if e["kind"] == "requirement":
            if not [r for r in e["in"] if r["kind"] == "realization" and E.get(r["source"], {}).get("level") == "abb"]:
                f("T4", eid, "no ABB realizes it")
            det = md.get(eid)
            if not det or not det["fm"].get("acceptance"):
                f("T5", eid, "no acceptance criteria (model/requirement/<id>.md)")
            elif not det["fm"].get("operational"):
                f("T5", eid, "no operational figures (latency, volume)")

    plateaus = [e for e in E.values() if e["kind"] == "plateau"]
    for p in plateaus:
        name = p["id"].split(".")[-1]
        if name not in PLATEAUS:
            f("P4", p["id"], f"plateau name '{name}' is not a plateau tag ({', '.join(PLATEAUS)})")
    for app in {p["application"] for p in plateaus}:
        chain = {p["id"] for p in plateaus if p["application"] == app}
        trig = {(r["source"], r["target"]) for r in bb["relations"] if r["kind"] == "triggering" and r["source"] in chain}
        names = [n for n in PLATEAUS if f"imp.{app}.{n}" in chain]
        for a, b in zip(names, names[1:]):
            if (f"imp.{app}.{a}", f"imp.{app}.{b}") not in trig:
                f("P4", f"imp.{app}.{a}", f"no triggering relationship to imp.{app}.{b}")

    parallel_changes(root, bb, f)

    checks = []
    for cid, group, title, sev in CHECKS:
        items = findings[cid]
        checks.append({"id": cid, "group": group, "title": title, "severity": sev,
                       "status": "pass" if not items else ("fail" if sev == "error" else "warn"), "items": items})

    arbs = {mid: arb_readiness(mid, m, bb, md, checks, schema) for mid, m in md.items() if m["fm"].get("level") == "arb"}
    summary = {"errors": sum(1 for c in checks if c["status"] == "fail"), "warnings": sum(1 for c in checks if c["status"] == "warn"),
               "passed": sum(1 for c in checks if c["status"] == "pass"),
               "bb": len(E), "markdown": len(md)}
    return bb, {"summary": summary, "checks": checks, "arbs": arbs}, md


def parallel_changes(root: Path, bb: dict, f) -> None:
    """C1–C4: one file per change, no conflicting retirements, declared order between overlapping changes."""
    E = bb["elements"]
    wps = {i: e for i, e in E.items() if e["kind"] == "work-package"}
    for path in sorted((root / "model" / "bb" / "changes").glob("*.c4")):
        names = re.findall(r"^\s+([\w-]+) = work-package\b", path.read_text(encoding="utf-8"), re.M)
        if len(names) != 1:
            f("C1", None, f"changes/{path.name}: {len(names)} work packages, expected 1")
        elif names[0] != path.stem:
            f("C1", None, f"changes/{path.name}: work package '{names[0]}' does not match the file name")

    order = bb.get("plateauOrder", {})

    def plateau_of(w):
        ps = [r["target"].split(".")[-1] for r in E[w]["out"] if r["kind"] == "realization" and E.get(r["target"], {}).get("kind") == "plateau"]
        app_order = order.get(E[w]["application"]) or PLATEAUS
        return min((app_order.index(p) for p in ps if p in app_order), default=None)

    deps = {}
    for w, e in wps.items():
        deps[w] = [d.strip() for d in (e["metadata"].get("dependsOn") or "").split(",") if d.strip()]
        for d in deps[w]:
            if d not in wps:
                f("C3", w, f"dependsOn '{d}', which is not a work package")
            elif plateau_of(d) is not None and plateau_of(w) is not None and plateau_of(d) > plateau_of(w):
                f("C3", w, f"dependsOn {d}, which delivers a later plateau")

    def reaches(a, b, seen=()):
        return any(d == b or (d not in seen and reaches(d, b, seen + (a,))) for d in deps.get(a, []))
    for w in wps:
        if reaches(w, w):
            f("C3", w, "circular dependsOn")

    for eid, e in E.items():
        if e["level"] not in ("abb", "sbb"):
            continue
        retiring = [r["source"] for r in e["in"] if r["source"] in wps and r["kind"] == "association" and r["title"].strip().lower() == "retires"]
        touching = [r["source"] for r in e["in"] if r["source"] in wps and r["kind"] == "realization"]
        if len(retiring) > 1:
            f("C2", eid, "retired by " + " and ".join(sorted(retiring)))
        for rw in retiring:
            for tw in touching:
                if plateau_of(tw) is not None and plateau_of(rw) is not None and plateau_of(tw) >= plateau_of(rw):
                    f("C2", eid, f"changed by {tw} after {rw} retires it")
        involved = sorted(set(retiring + touching))
        for i, a in enumerate(involved):
            for b in involved[i + 1:]:
                if not (reaches(a, b) or reaches(b, a)):
                    f("C4", eid, f"touched by {a} and {b} without dependsOn between them")


def arb_readiness(mid: str, m: dict, bb: dict, md: dict, checks: list, schema: dict) -> dict:
    """What the board needs: scope of the change, checks on that scope, ASD completeness, reviewer decisions."""
    fm = m["fm"]
    a, b = fm.get("from", "").split(".")[-1], fm.get("to", "").split(".")[-1]
    scope = [g for g in gap(bb, a, b) if g["change"] != "unchanged"]
    scope_ids = {g["id"] for g in scope}
    # DD and requirement files belonging to the scope are in scope too
    for did, d in md.items():
        if d["fm"].get("level") == "dd" and set(d["fm"].get("realizes") or []) & scope_ids:
            scope_ids.add(did)
    scope_ids |= set(fm.get("requirements") or [])
    scoped = []
    for c in checks:
        items = [i for i in c["items"] if i["id"] in scope_ids]
        scoped.append({"id": c["id"], "group": c["group"], "title": c["title"], "severity": c["severity"],
                       "status": "pass" if not items else ("fail" if c["severity"] == "error" else "warn"), "items": items})
    body = m["body"]
    heads = {h.strip(): sec for h, sec in re.findall(r"^## (.+?)\n(.*?)(?=^## |\Z)", body, flags=re.S | re.M)}
    sections = []
    for s in schema["$defs"]["asdSections"]:
        content = heads.get(s, "").strip()
        sections.append({"title": s, "status": "complete" if len(content) > 80 else ("thin" if content else "missing")})
    reviewers = fm.get("reviewers") or []
    pending = [r for r in reviewers if r["decision"] == "pending"]
    blocking = [r for r in reviewers if r["decision"] in ("changes-requested", "rejected")]
    open_conditions = [c for c in fm.get("conditions") or [] if c["status"] == "open"]
    errors = sum(1 for c in scoped if c["status"] == "fail")
    warnings = sum(1 for c in scoped if c["status"] == "warn")
    missing = [s["title"] for s in sections if s["status"] == "missing"]
    if errors or missing:
        readiness = "blocked"
    elif warnings or blocking or pending or open_conditions:
        readiness = "attention"
    else:
        readiness = "ready"
    return {"scope": scope, "checks": scoped, "sections": sections, "readiness": readiness,
            "counts": {"errors": errors, "warnings": warnings, "pending": len(pending), "changesRequested": len(blocking),
                       "openConditions": len(open_conditions), "inScope": len(scope)}}


def main() -> int:
    bb, report, md = run(ROOT)
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    (dist / "bb.json").write_text(json.dumps(bb, indent=1, ensure_ascii=False), encoding="utf-8")
    (dist / "validation.json").write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    s = report["summary"]
    print(f"building blocks: {s['bb']} · markdown files: {s['markdown']}")
    for c in report["checks"]:
        mark = {"pass": "ok  ", "warn": "WARN", "fail": "FAIL"}[c["status"]]
        print(f"  {mark} {c['id']} {c['title']}")
        for i in c["items"]:
            print(f"         - {i['id'] or ''}: {i['message']}")
    for aid, a in report["arbs"].items():
        print(f"ARB {aid}: {a['readiness']} · {a['counts']}")
    print(f"{s['passed']} passed · {s['warnings']} warnings · {s['errors']} errors")
    return 1 if s["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
