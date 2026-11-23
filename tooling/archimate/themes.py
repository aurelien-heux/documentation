"""Renderer themes generated from the notation data: aitoolbox.puml (PlantUML include) and aitoolbox-mermaid.json."""
import json
GLYPHS = json.load(open("glyph_paths.json"))
from axdata import ROLES, LAYERS, ELEMENTS, RELATIONSHIPS, PERFORMERS, CHANGE, VERSION

BEHAVIOUR_STEREOS = [e["puStereo"] for e in ELEMENTS if e["shape"] == "rounded" and e["puStereo"]]
VAR = {  # PlantUML variable name -> role key
    "TEXT": "text", "MUTED": "muted", "LINE": "line", "OUTLINE": "outline", "OUTLINE_VARIANT": "outlineVariant",
    "CANVAS": "canvas", "LANE": "lane", "NOTE": "note", "HIGHEST": "highest", "LOWEST": "lowest",
    "PRIMARY": "primary", "PRIMARY_CONTAINER": "primaryContainer", "ON_PRIMARY_CONTAINER": "onPrimaryContainer",
    "AI": "ai", "AI_CONTAINER": "aiContainer", "ON_AI_CONTAINER": "onAiContainer",
    "SUCCESS": "success", "SUCCESS_CONTAINER": "successContainer", "ON_SUCCESS_CONTAINER": "onSuccessContainer",
    "WARNING": "warning", "WARNING_CONTAINER": "warningContainer", "ON_WARNING_CONTAINER": "onWarningContainer",
    "ERROR": "error", "ERROR_CONTAINER": "errorContainer", "ON_ERROR_CONTAINER": "onErrorContainer",
}


def layer_colours(theme):
    return {l["id"]: l[theme] for l in LAYERS}


def sprite_name(eid):
    return "$axg_" + eid.replace("-", "_")


def puml_sprites(theme):
    out = []
    for e in ELEMENTS:
        if e["shape"] in ("group", "junction"):
            continue
        ink = next(l for l in LAYERS if l["id"] == e["layer"])[theme]["ink"]
        body = "".join(
            f'<path d="{p["d"]}" fill="{ink}" stroke="none"/>' if p["filled"] else
            f'<path d="{p["d"]}" fill="none" stroke="{ink}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'
            + (f' stroke-dasharray="{p["dash"]}"' if p["dash"] else "") + "/>"
            for p in GLYPHS[e["id"]])
        svg = '<svg viewBox="0 0 24 24" width="18" height="18">' + body + "</svg>"
        out.append(f"sprite {sprite_name(e['id'])} {svg}")
    return out


def puml_vars(theme):
    r = ROLES[theme]
    out = [f'!$AX_{k} = "{r[v]}"' for k, v in VAR.items()]
    out += [f'!$AX_{k}_NH = "{r[v].lstrip("#")}"' for k, v in VAR.items() if k in ("OUTLINE", "OUTLINE_VARIANT", "PRIMARY", "AI")]
    for lid, c in layer_colours(theme).items():
        out.append(f'!$AX_{lid.upper()}_FILL = "{c["fill"]}"')
        out.append(f'!$AX_{lid.upper()}_INK = "{c["ink"].lstrip("#")}"')   # without # : the form PlantUML takes after line:
        out.append(f'!$AX_{lid.upper()}_INKC = "{c["ink"]}"')
    return out


def puml_theme():
    L = []
    L += ["' aitoolbox.puml: AIToolbox notation theme for PlantUML (" + VERSION + ").",
          "' Generated from the design system: do not edit, change the design system and regenerate.",
          "' Dark theme: !$AX_THEME = \"dark\" before the include. Default: light.",
          "' Elements: AX_<Type>(alias, \"label\"), e.g. AX_BusinessProcess(PRC04, \"Change the model\"). Agents: AX_Agent.",
          "' Relationships: AX_Rel<Type>(from, to, \"label\", dir) with dir up | down | left | right (optional). Workflow steps: AX_Step(\"label\", by, change).",
          "' Layout: Smetana, built into PlantUML: no Graphviz install, and the in-browser engine needs no WebAssembly.",
          "!pragma layout smetana",
          '!if %not(%variable_exists("$AX_THEME"))', '!$AX_THEME = "light"', "!endif",
          '!if ($AX_THEME == "dark")']
    L += ["  " + x for x in puml_vars("dark")] + puml_sprites("dark")
    L += ["!else"] + ["  " + x for x in puml_vars("light")] + puml_sprites("light") + ["!endif", ""]
    rounded = ", ".join("." + s for s in BEHAVIOUR_STEREOS)
    L += ["<style>",
          "root { FontName \"Open Sans\"; FontSize 13; FontColor $AX_TEXT; LineColor $AX_LINE; BackgroundColor $AX_CANVAS; HyperlinkColor $AX_PRIMARY }",
          "document { BackgroundColor $AX_CANVAS }",
          "title { FontSize 15; FontStyle bold; FontColor $AX_TEXT; LineThickness 0; BackgroundColor transparent; Margin 4 }",
          "caption { FontSize 11; FontColor $AX_MUTED }",
          "legend { BackgroundColor $AX_NOTE; LineColor $AX_OUTLINE_VARIANT; FontSize 11; FontColor $AX_TEXT }",
          "note { BackgroundColor $AX_NOTE; LineColor $AX_OUTLINE_VARIANT; FontSize 12; FontColor $AX_TEXT }",
          "arrow { LineColor $AX_LINE; FontColor $AX_MUTED; FontSize 11; LineThickness 1.2 }",
          "archimate { LineThickness 1; FontSize 13; Padding 6 }",
          ".ax-rounded { RoundCorner 24 }",
          ".ax-ellipse { RoundCorner 60 }",
          "rectangle { LineColor $AX_OUTLINE_VARIANT; BackgroundColor transparent; FontColor $AX_MUTED; FontSize 12 }",
          ".grouping { LineStyle 6-4; LineColor $AX_OTHER_INKC; BackgroundColor transparent; FontColor $AX_TEXT }",
          ".layer { LineStyle 0; LineColor $AX_OUTLINE_VARIANT; BackgroundColor transparent; FontColor $AX_MUTED; FontStyle bold; FontSize 11 }",
          "circle { BackgroundColor $AX_TEXT; LineColor $AX_TEXT }",
          ".or { BackgroundColor $AX_CANVAS }",
          "activityDiagram {",
          "  activity { BackgroundColor $AX_LOWEST; LineColor $AX_OUTLINE; FontColor $AX_TEXT; RoundCorner 16; FontSize 13; Padding 6 }",
          "  diamond { BackgroundColor $AX_LOWEST; LineColor $AX_OUTLINE; FontColor $AX_TEXT; FontSize 12 }",
          "  swimlane { TitleFontSize 13; TitleFontStyle bold; TitleFontColor $AX_TEXT; LineColor $AX_OUTLINE_VARIANT }",
          "  partition { LineColor $AX_OUTLINE_VARIANT; FontColor $AX_MUTED }",
          "  circle { BackgroundColor $AX_TEXT; LineColor $AX_TEXT }",
          "  arrow { LineColor $AX_LINE; FontColor $AX_MUTED; FontSize 11 }",
          "}",
          "stateDiagram {",
          "  state { BackgroundColor $AX_LOWEST; LineColor $AX_OUTLINE; FontColor $AX_TEXT; RoundCorner 16; FontSize 13 }",
          "  arrow { LineColor $AX_LINE; FontColor $AX_MUTED; FontSize 11 }",
          "}",
          "classDiagram {",
          "  class { BackgroundColor $AX_APPLICATION_FILL; LineColor $AX_APPLICATION_INKC; FontColor $AX_TEXT; FontSize 12; RoundCorner 0 }",
          "  arrow { LineColor $AX_LINE; FontColor $AX_MUTED; FontSize 11 }",
          "}",
          "sequenceDiagram {",
          "  participant { BackgroundColor $AX_APPLICATION_FILL; LineColor $AX_APPLICATION_INKC; FontColor $AX_TEXT; FontSize 13 }",
          "  actor { BackgroundColor $AX_LOWEST; LineColor $AX_OUTLINE; FontColor $AX_TEXT }",
          "  lifeLine { LineColor $AX_OUTLINE_VARIANT; BackgroundColor $AX_HIGHEST }",
          "  group { LineColor $AX_OUTLINE; FontColor $AX_TEXT; BackgroundColor transparent }",
          "  groupHeader { FontColor $AX_TEXT; LineColor $AX_OUTLINE }",
          "  arrow { LineColor $AX_LINE; FontColor $AX_TEXT; FontSize 12 }",
          "  reference { LineColor $AX_OUTLINE; BackgroundColor $AX_NOTE }",
          "}",
          "componentDiagram {",
          "  component { BackgroundColor $AX_APPLICATION_FILL; LineColor $AX_APPLICATION_INKC; FontColor $AX_TEXT; FontSize 13; LineThickness 1 }",
          "  interface { BackgroundColor $AX_LOWEST; LineColor $AX_APPLICATION_INKC; FontColor $AX_TEXT; FontSize 12; LineThickness 1.5 }",
          "}",
          "' who performs a step",
          ".agent { BackgroundColor $AX_AI_CONTAINER; LineColor $AX_AI; FontColor $AX_ON_AI_CONTAINER }",
          ".system { BackgroundColor $AX_HIGHEST; LineColor $AX_OUTLINE_VARIANT; FontColor $AX_TEXT }",
          ".external { BackgroundColor $AX_HIGHEST; LineColor $AX_OUTLINE; FontColor $AX_TEXT; LineThickness 1 }",
          ".gate { BackgroundColor $AX_PRIMARY_CONTAINER; LineColor $AX_PRIMARY; LineThickness 2; FontColor $AX_ON_PRIMARY_CONTAINER }",
          ".event { BackgroundColor $AX_BUSINESS_FILL; LineColor $AX_BUSINESS_INKC; FontColor $AX_TEXT }",
          "' change marks",
          ".added { BackgroundColor $AX_SUCCESS_CONTAINER; LineColor $AX_SUCCESS; FontColor $AX_ON_SUCCESS_CONTAINER }",
          ".changed { BackgroundColor $AX_WARNING_CONTAINER; LineColor $AX_WARNING; FontColor $AX_ON_WARNING_CONTAINER }",
          ".moved { BackgroundColor $AX_PRIMARY_CONTAINER; LineColor $AX_PRIMARY; FontColor $AX_ON_PRIMARY_CONTAINER; LineStyle 2-2 }",
          ".removed { BackgroundColor $AX_ERROR_CONTAINER; LineColor $AX_ERROR; FontColor $AX_ON_ERROR_CONTAINER; LineStyle 5-4 }",
          "' state machine: the state an instance is in now",
          ".current { BackgroundColor $AX_PRIMARY_CONTAINER; LineColor $AX_PRIMARY; LineThickness 2; FontColor $AX_ON_PRIMARY_CONTAINER }",
          "' detailed design",
          ".root { LineThickness 2 }",
          ".valueobject { BackgroundColor $AX_HIGHEST; LineColor $AX_OUTLINE }",
          ".enumeration { BackgroundColor $AX_HIGHEST; LineColor $AX_OUTLINE }",
          "</style>",
          "skinparam shadowing false",
          "skinparam ArrowFontName \"Open Sans\"",
          "skinparam defaultTextAlignment center",
          ""]
    # elements
    for e in ELEMENTS:
        if e["shape"] in ("group", "junction"):
            continue
        lay = e["layer"].upper()
        L += [f'!procedure {e["pu"]}($alias, $label)',
              f'archimate $AX_{lay}_FILL;line:$AX_{lay}_INK "<{sprite_name(e["id"])}>\\n$label" as $alias <<ax-{e["shape"]}>>', "!endprocedure"]
    L += ['!procedure AX_Agent($alias, $label)',
          'archimate $AX_APPLICATION_FILL;line:$AX_APPLICATION_INK "<$axg_application_component>\\n$label\\n<size:10>✦ agent</size>" as $alias <<ax-rect>>',
          "!endprocedure",
          '!procedure AX_Junction($alias, $kind="and")',
          '!if ($kind == "or")', 'circle " " as $alias <<or>>', "!else", 'circle " " as $alias', "!endif", "!endprocedure",
          '!procedure AX_Group($alias, $label)', 'rectangle "$label" as $alias <<grouping>> {', "!endprocedure",
          '!procedure AX_Layer($alias, $label)', 'rectangle "$label" as $alias <<layer>> {', "!endprocedure",
          "!procedure AX_End()", "}", "!endprocedure", ""]
    for r in RELATIONSHIPS:
        arrow = r["puDir"].replace("{d}", "$dir")
        L += [f'!procedure {r["proc"]}($from, $to, $label="", $dir="")',
              '!if ($label == "")', f'$from {arrow} $to', "!else", f'$from {arrow} $to : $label', "!endif", "!endprocedure"]
    # workflow
    L += ["",
          "' Workflow step. by: human (default) | agent | system | gate | event. change: added | changed | moved | removed",
          '!procedure AX_Step($label, $by="human", $change="")',
          '!$mark = ""',
          '!if ($by == "agent")', '!$mark = "<size:10>✦ agent</size>\\n"',
          '!elseif ($by == "system")', '!$mark = "<size:10>system</size>\\n"',
          '!elseif ($by == "gate")', '!$mark = "<size:10>review gate</size>\\n"',
          '!elseif ($by == "event")', '!$mark = "<size:10>event</size>\\n"', "!endif",
          '!$cls = $by',
          '!if ($change == "added")', '!$text = "+ " + $label', '!$cls = "added"',
          '!elseif ($change == "changed")', '!$text = "Δ " + $label', '!$cls = "changed"',
          '!elseif ($change == "moved")', '!$text = "↕ " + $label', '!$cls = "moved"',
          '!elseif ($change == "removed")', '!$text = "− <s>" + $label + "</s>"', '!$cls = "removed"',
          "!else", "!$text = $label", "!endif",
          '!if ($cls == "human")', ':$mark$text;', "!else", ':$mark$text; <<$cls>>', "!endif",
          "!endprocedure",
          '!procedure AX_Gate($label, $change="")', 'AX_Step($label, "gate", $change)', "!endprocedure",
          '!procedure AX_Event($label, $change="")', 'AX_Step($label, "event", $change)', "!endprocedure",
          ]
    return "\n".join(L) + "\n"


def mermaid_theme():
    out = {"version": VERSION, "usage": "mermaid.initialize(theme.light.config) or the config file of mermaid-cli; append theme.<mode>.classDefs to every flowchart and state diagram.", "light": {}, "dark": {}}
    for th in ("light", "dark"):
        r = ROLES[th]
        tv = dict(darkMode=th == "dark", background=r["canvas"], fontFamily="'Open Sans', system-ui, sans-serif", fontSize="13px",
                  primaryColor=r["lowest"], primaryBorderColor=r["outline"], primaryTextColor=r["text"],
                  secondaryColor=r["highest"], secondaryBorderColor=r["outlineVariant"], secondaryTextColor=r["text"],
                  tertiaryColor=r["lane"], tertiaryBorderColor=r["outlineVariant"], tertiaryTextColor=r["text"],
                  lineColor=r["line"], textColor=r["text"], titleColor=r["text"], edgeLabelBackground=r["canvas"],
                  clusterBkg=r["lane"], clusterBorder=r["outlineVariant"], nodeBorder=r["outline"], mainBkg=r["lowest"],
                  noteBkgColor=r["note"], noteBorderColor=r["outlineVariant"], noteTextColor=r["text"],
                  actorBkg=r["lowest"], actorBorder=r["outline"], actorTextColor=r["text"], actorLineColor=r["outlineVariant"],
                  signalColor=r["line"], signalTextColor=r["text"], labelBoxBkgColor=r["note"], labelBoxBorderColor=r["outline"],
                  labelTextColor=r["text"], loopTextColor=r["text"], activationBkgColor=r["highest"], activationBorderColor=r["outline"],
                  sequenceNumberColor=r["canvas"],
                  stateBkg=r["lowest"], stateBorder=r["outline"], transitionColor=r["line"], transitionLabelColor=r["muted"],
                  stateLabelColor=r["text"], specialStateColor=r["text"], innerEndBackground=r["text"], compositeBackground=r["lane"],
                  compositeTitleBackground=r["lane"], altBackground=r["lane"],
                  classText=r["text"], attributeBackgroundColorOdd=r["lowest"], attributeBackgroundColorEven=r["lane"],
                  relationColor=r["line"], relationLabelColor=r["muted"], relationLabelBackground=r["canvas"])
        lc = layer_colours(th)
        cd = {}
        for lid, c in lc.items():
            cd[lid] = f'fill:{c["fill"]},stroke:{c["ink"]},stroke-width:1px,color:{r["text"]}'
        cd.update({
            "human": f'fill:{r["lowest"]},stroke:{r["outline"]},stroke-width:1px,color:{r["text"]}',
            "agent": f'fill:{r["aiContainer"]},stroke:{r["ai"]},stroke-width:1px,color:{r["onAiContainer"]}',
            "system": f'fill:{r["highest"]},stroke:{r["outlineVariant"]},stroke-width:1px,color:{r["text"]}',
            "external": f'fill:{r["highest"]},stroke:{r["outline"]},stroke-width:1px,color:{r["text"]}',
            "gate": f'fill:{r["primaryContainer"]},stroke:{r["primary"]},stroke-width:2px,color:{r["onPrimaryContainer"]}',
            "event": f'fill:{lc["business"]["fill"]},stroke:{lc["business"]["ink"]},stroke-width:1px,color:{r["text"]}',
            "decision": f'fill:{r["lowest"]},stroke:{r["outline"]},stroke-width:1px,color:{r["text"]}',
            "added": f'fill:{r["successContainer"]},stroke:{r["success"]},stroke-width:1px,color:{r["onSuccessContainer"]}',
            "changed": f'fill:{r["warningContainer"]},stroke:{r["warning"]},stroke-width:1px,color:{r["onWarningContainer"]}',
            "moved": f'fill:{r["primaryContainer"]},stroke:{r["primary"]},stroke-width:1px,stroke-dasharray:2 2,color:{r["onPrimaryContainer"]}',
            "removed": f'fill:{r["errorContainer"]},stroke:{r["error"]},stroke-width:1px,stroke-dasharray:5 4,color:{r["onErrorContainer"]}',
            "current": f'fill:{r["primaryContainer"]},stroke:{r["primary"]},stroke-width:2px,color:{r["onPrimaryContainer"]}',
            "grouping": f'fill:none,stroke:{lc["other"]["ink"]},stroke-width:1.5px,stroke-dasharray:6 4,color:{r["text"]}',
            "lane": f'fill:{r["lane"]},stroke:{r["outlineVariant"]},stroke-width:1px,color:{r["text"]}',
            "layer": f'fill:none,stroke:{r["outlineVariant"]},stroke-width:1px,color:{r["muted"]}',
            "valueobject": f'fill:{r["highest"]},stroke:{r["outline"]},stroke-width:1px,color:{r["text"]}',
            "root": f'fill:{lc["application"]["fill"]},stroke:{lc["application"]["ink"]},stroke-width:2px,color:{r["text"]}',
            "entity": f'fill:{lc["application"]["fill"]},stroke:{lc["application"]["ink"]},stroke-width:1px,color:{r["text"]}',
        })
        out[th] = {"config": {"theme": "base", "themeVariables": tv, "flowchart": {"htmlLabels": True, "curve": "basis", "padding": 12},
                              "sequence": {"mirrorActors": False, "showSequenceNumbers": False, "actorFontFamily": "'Open Sans', system-ui, sans-serif"},
                              "state": {"defaultRenderer": "dagre-wrapper"}, "er": {"layoutDirection": "LR"}},
                   "classDefs": [f"classDef {k} {v}" for k, v in cd.items()]}
    return out


if __name__ == "__main__":
    import os
    os.makedirs("out/themes", exist_ok=True)
    open("out/themes/aitoolbox.puml", "w").write(puml_theme())
    json.dump(mermaid_theme(), open("out/themes/aitoolbox-mermaid.json", "w"), indent=1, ensure_ascii=False)
    print("ok")
