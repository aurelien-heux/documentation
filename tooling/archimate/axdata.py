"""AIToolbox notation 2.0 — the data of the ArchiMate design system: layers, element types, relationships, change marks,
diagram kinds and components. Diagrams are generated from YAML views as PlantUML or Mermaid (DEC-14); LikeC4 is no
longer used. Tokens: AIToolbox 5.0.1."""
import json

VERSION = "Notation 2.0 · tokens 5.0.1 · PlantUML 1.2026.8 · Mermaid 11.16"

OLD = json.load(open("notation-1x.json"))
LAYERS = OLD["layers"]
LAYER = {l["id"]: l for l in LAYERS}

# --- colour roles used by diagrams (tokens 5.0.1) ------------------------------------------------------------------
ROLES = {
    "light": dict(text="#1C1B1E", muted="#48454E", line="#48454E", outline="#79757F", outlineVariant="#CAC4CF",
                  canvas="#FFFFFF", lane="#FAF4FF", note="#F2EBFA", highest="#ECE5F4", lowest="#FFFFFF",
                  primary="#39235F", primaryContainer="#E3DFFF", onPrimaryContainer="#14085E",
                  ai="#004F50", aiContainer="#9CF1F0", onAiContainer="#002020",
                  success="#0B5314", successContainer="#ACF4A2", onSuccessContainer="#002203",
                  warning="#5C4300", warningContainer="#FFDEA0", onWarningContainer="#261900",
                  error="#93000A", errorContainer="#FFDAD6", onErrorContainer="#410002"),
    "dark": dict(text="#ECE5F8", muted="#CAC3DC", line="#CAC3DC", outline="#948DA5", outlineVariant="#494458",
                 canvas="#14121E", lane="#1D1A27", note="#2B2836", highest="#363341", lowest="#0F0C19",
                 primary="#C4C0FF", primaryContainer="#413C8A", onPrimaryContainer="#E3DFFF",
                 ai="#80D5D4", aiContainer="#004F50", onAiContainer="#9CF1F0",
                 success="#91D888", successContainer="#0B5314", onSuccessContainer="#ACF4A2",
                 warning="#FCBC00", warningContainer="#5C4300", onWarningContainer="#FFDEA0",
                 error="#FFB4AB", errorContainer="#93000A", onErrorContainer="#FFDAD6"),
}

# --- element types ----------------------------------------------------------------------------------------------------
# YAML type names and ID prefixes kept by the Preliminary (2026-11-19): the vocabulary of the model.
MODEL = {
    "stakeholder": ("stakeholder", "STK"), "driver": ("driver", "DRV"), "assessment": ("assessment", "ASM"),
    "goal": ("goal", "GOL"), "outcome": ("outcome", "OUT"), "principle": ("principle", "PRI"),
    "requirement": ("requirement", "REQ"), "constraint": ("constraint", "CON"),
    "capability": ("capability", "CAP"), "value-stream": ("value-stream", "VST"),
    "business-actor": ("actor", "ACT"), "business-role": ("role", "ROL"), "business-process": ("process", "PRC"),
    "business-function": ("function", "FUN"), "business-event": ("event", "EVT"),
    "business-service": ("business-service", "BSV"), "business-object": ("business-object", "BOB"),
    "application-component": ("application-component", "APC"), "application-service": ("application-service", "APS"),
    "application-interface": ("application-interface", "API"), "data-object": ("data-object", "DOB"),
}
PU_STEREO = json.load(open("pu_stereo.json"))
PU_STEREO.update({"value-stream": "strategy-valuestream", "work-package": "implementation-workpackage"})
MM_SHAPE = {"rect": "rect", "rounded": "rounded", "object": "div-rect", "contract": "div-rect", "wave": "doc",
            "product": "rect", "artifact": "tag-rect", "chamfer": "notch-rect", "ellipse": "stadium", "group": "subgraph",
            "junction": "sm-circ"}


def proc_name(eid):
    return "AX_" + "".join(p.capitalize() for p in eid.split("-"))


ELEMENTS = []
for e in OLD["elements"]:
    m = MODEL.get(e["id"])
    ELEMENTS.append(dict(
        id=e["id"], name=e["name"], layer=e["layer"], aspect=e["aspect"], shape=e["shape"], svg=e["svg"],
        definition=e["definition"], inModel=bool(m), yaml=m[0] if m else "", prefix=m[1] if m else "",
        pu=proc_name(e["id"]) if e["shape"] not in ("group", "junction") else ("AX_Group" if e["shape"] == "group" else "AX_Junction"),
        puStereo=PU_STEREO.get(e["id"], ""), mm=MM_SHAPE[e["shape"]]))
EL = {e["id"]: e for e in ELEMENTS}

# --- relationships ----------------------------------------------------------------------------------------------------
# PlantUML arrows draw the ArchiMate markers; Mermaid cannot, so its edges keep the line style and name the type.
REL_PU = {"composition": "*-{d}-", "aggregation": "o-{d}-", "assignment": "@-{d}->", "realization": ".{d}.|>",
          "serving": "-{d}->", "access": "-[dotted]{d}->", "influence": "-[dashed]{d}->", "triggering": "-{d}->>",
          "flow": "-[dashed]{d}->>", "specialization": "-{d}-|>", "association": "-{d}-"}
REL_MM = {"composition": "-->", "aggregation": "-->", "assignment": "-->", "realization": "-.->",
          "serving": "-->", "access": "-.->", "influence": "-.->", "triggering": "==>", "flow": "-.->",
          "specialization": "-->", "association": "---"}
KEPT_RELS = ["composition", "aggregation", "assignment", "realization", "serving", "access", "influence",
             "triggering", "flow", "association"]
RELATIONSHIPS = []
for r in OLD["relationships"]:
    RELATIONSHIPS.append(dict(id=r["id"], name=r["name"], line=r["line"], source=r["source"], target=r["target"],
                              definition=r["definition"], pu=REL_PU[r["id"]].replace("{d}", ""), puDir=REL_PU[r["id"]], mm=REL_MM[r["id"]],
                              inModel=r["id"] in KEPT_RELS, proc="AX_Rel" + r["name"].replace(" ", "")))

# --- change marks (process change, gap tables, element headers) ---------------------------------------------------
CHANGE = [
    dict(id="added", label="Added", glyph="+", role="success", meaning="In the target only."),
    dict(id="changed", label="Changed", glyph="Δ", role="warning", meaning="In both, with a different name, performer, rule or input."),
    dict(id="moved", label="Moved", glyph="↕", role="primary", meaning="In both, at another place in the flow or in another lane. Process change only."),
    dict(id="removed", label="Removed", glyph="−", role="error", meaning="In the baseline only. Drawn dashed and struck through, where it was."),
    dict(id="unchanged", label="Unchanged", glyph="=", role="neutral", meaning="In both, the same. Shown without a mark; the chip appears in tables only."),
]

# --- who performs a step (workflow, sequence) ----------------------------------------------------------------------
PERFORMERS = [
    dict(id="human", label="Person", mark="", fill="lowest", ink="outline", text="text",
         rule="A role in the lane title does it. No mark: people are the default."),
    dict(id="agent", label="Agent", mark="✦ agent", fill="aiContainer", ink="ai", text="onAiContainer",
         rule="An application component with agent: true does it. Teal AI container and the ✦ agent line, never teal alone."),
    dict(id="system", label="System", mark="system", fill="highest", ink="outlineVariant", text="text",
         rule="A non-agent application component or an external system (Jenkins, Git hosting) does it."),
    dict(id="gate", label="Review gate", mark="review gate", fill="primaryContainer", ink="primary", text="onPrimaryContainer",
         rule="A named person approves an agent output before it takes effect (PRI-01). 2 px primary border and the review gate line."),
    dict(id="event", label="Event", mark="event", fill="business", ink="business", text="text",
         rule="What starts or ends the flow: an ArchiMate business event, in business colours."),
]
