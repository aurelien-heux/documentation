"""Sample diagrams of every kind, for the design-system page: the YAML view, the PlantUML source and the Mermaid source.
Layered views are generated from the YAML (as the view generator will); the other kinds are written once per renderer
in the shape the generator will emit them. Domain: AI Toolbox's own architecture work (TOGAF framing, 2026-11-19)."""
import yaml
from axdata import EL, RELATIONSHIPS

REL = {r["id"]: r for r in RELATIONSHIPS}
YAML_TYPE = {e["yaml"]: e["id"] for e in EL.values() if e["yaml"]}

# ---------------------------------------------------------------------------------------------------------------------
LAYERED_MODEL = """\
# model/*.yaml (excerpt)
- {id: GOL-01, type: goal, name: Productivity and developer experience}
- {id: REQ-05, type: requirement, name: Reviewed knowledge in one repository}
- {id: CAP-03, type: capability, name: Architecture management}
- {id: ROL-02, type: role, name: Lead architect}
- {id: EVT-02, type: event, name: Change requested}
- {id: PRC-04, type: process, name: Change the architecture model}
- {id: BOB-03, type: business-object, name: Architecture change}
- {id: APC-07, type: application-component, name: Architecture agent, agent: true}
- {id: APC-02, type: application-component, name: Knowledge base}
- {id: APS-05, type: application-service, name: Model validation}
- {id: DOB-04, type: data-object, name: Architecture model}
"""
LAYERED_VIEW = """\
# views/architecture-change.yaml
id: VIEW-07
kind: layered
title: Changing the architecture model
renderer: plantuml            # plantuml | mermaid
elements: [GOL-01, REQ-05, CAP-03, ROL-02, EVT-02, PRC-04, BOB-03, APC-07, APC-02, APS-05, DOB-04]
relations:
  - {type: realization, from: REQ-05, to: GOL-01}
  - {type: realization, from: CAP-03, to: REQ-05}
  - {type: realization, from: PRC-04, to: CAP-03}
  - {type: assignment, from: ROL-02, to: PRC-04}
  - {type: triggering, from: EVT-02, to: PRC-04}
  - {type: access, from: PRC-04, to: BOB-03}
  - {type: serving, from: APC-07, to: PRC-04, label: drafts the update}
  - {type: serving, from: APS-05, to: PRC-04}
  - {type: realization, from: APC-02, to: APS-05}
  - {type: realization, from: DOB-04, to: BOB-03}
  - {type: access, from: APC-07, to: DOB-04, label: writes}
"""
LAYER_ORDER = ["motivation", "strategy", "business", "application", "technology", "physical", "implementation", "other"]
LAYER_TITLE = {"motivation": "Motivation", "strategy": "Strategy", "business": "Business", "application": "Application",
               "technology": "Technology", "physical": "Physical", "implementation": "Implementation & migration", "other": "Other"}


def gen_layered():
    model = {x["id"]: x for x in yaml.safe_load(LAYERED_MODEL)}
    view = yaml.safe_load(LAYERED_VIEW)
    els = [model[i] for i in view["elements"]]
    alias = lambda i: i.replace("-", "")
    by_layer = {}
    for x in els:
        e = EL[YAML_TYPE[x["type"]]]
        by_layer.setdefault(e["layer"], []).append((x, e))
    pu = ["@startuml", "!include aitoolbox.puml", "hide stereotype", f'title {view["title"]}', ""]
    mm = ["flowchart TB"]
    for lay in LAYER_ORDER:
        if lay not in by_layer:
            continue
        pu.append(f'AX_Layer(L_{lay}, "{LAYER_TITLE[lay]}")')
        mm.append(f'  subgraph L_{lay}["{LAYER_TITLE[lay]}"]')
        mm.append("    direction LR")
        for x, e in by_layer[lay]:
            a = alias(x["id"])
            label = f'{x["name"]}'
            if x.get("agent"):
                pu.append(f'  AX_Agent({a}, "{label}")')
                mm.append(f'    {a}@{{ shape: {e["mm"]}, label: "{label}<br><small>✦ agent</small>" }}')
            else:
                pu.append(f'  {e["pu"]}({a}, "{label}")')
                mm.append(f'    {a}@{{ shape: {e["mm"]}, label: "{label}" }}')
        pu.append("AX_End()")
        mm.append("  end")
    pu.append("")
    for r in view["relations"]:
        rr = REL[r["type"]]
        lab = r.get("label", "")
        up = LAYER_ORDER.index(EL[YAML_TYPE[model[r["to"]]["type"]]]["layer"]) < LAYER_ORDER.index(EL[YAML_TYPE[model[r["from"]]["type"]]]["layer"])
        args = [alias(r["from"]), alias(r["to"])] + ([f'"{lab}"'] if lab or up else []) + (['"up"'] if up else [])
        pu.append(f'{rr["proc"]}(' + ", ".join(args) + ")")
        mmlab = (r["type"] + (": " + lab if lab else ""))
        edge = rr["mm"]
        mm.append(f'  {alias(r["from"])} {edge}|{mmlab}| {alias(r["to"])}')
    pu.append("@enduml")
    for lay in by_layer:
        mm.append(f'  class {",".join(alias(x["id"]) for x, _ in by_layer[lay])} {lay}')
        mm.append(f'  class L_{lay} layer')
    return "\n".join(pu), "\n".join(mm), LAYERED_MODEL + "\n" + LAYERED_VIEW


# ---------------------------------------------------------------------------------------------------------------------
WORKFLOW_VIEW = """\
# views/change-the-model.yaml: the steps of PRC-04, in order, with who does them
id: VIEW-08
kind: workflow
process: PRC-04
renderer: plantuml
lanes: [ROL-01 Requester, APC-07 Architecture agent, APC-09 Jenkins, ROL-02 Lead architect]
steps:
  - {event: EVT-02, name: Change requested, lane: ROL-01}
  - {name: Describe the change in chat, lane: ROL-01}
  - {name: Draft the model update, lane: APC-07, by: agent}
  - {name: Validate schema and references, lane: APC-09, by: system,
     until: {question: Checks pass?, no: Fix the findings}}
  - {name: Review the pull request, lane: ROL-02, gate: true, reads: Pull request,
     decision: {question: Approved?, no: {go: Draft the model update, label: changes requested}}}
  - {name: Merge and publish, lane: APC-09, by: system}
  - {event: EVT-03, name: Model updated, lane: APC-09}
"""
WORKFLOW_PU = """\
@startuml
!include aitoolbox.puml
title Change the architecture model (PRC-04)
|Requester|
start
AX_Event("Change requested")
AX_Step("Describe the change in chat")
|Architecture agent|
repeat
  repeat
    AX_Step("Draft or fix the model update", "agent")
    |Jenkins|
    AX_Step("Validate schema and references", "system")
  repeat while (Checks pass?) is (no) not (yes)
  |Lead architect|
  AX_Gate("Review the pull request")
  note right: Pull request
repeat while (Approved?) is (changes requested) not (approved)
|Jenkins|
AX_Step("Merge and publish", "system")
AX_Event("Model updated")
stop
@enduml"""
WORKFLOW_MM = """\
flowchart TB
  s0@{ shape: sm-circ, label: " " }
  e1@{ shape: rounded, label: "<small>Requester · event</small><br>Change requested" }
  s1@{ shape: rounded, label: "<small>Requester</small><br>Describe the change in chat" }
  s2@{ shape: rounded, label: "<small>✦ Architecture agent</small><br>Draft or fix the model update" }
  s4@{ shape: rounded, label: "<small>Jenkins · system</small><br>Validate schema and references" }
  d1@{ shape: diam, label: "Checks pass?" }
  s5@{ shape: rounded, label: "<small>Lead architect · review gate</small><br>Review the pull request" }
  o1@{ shape: div-rect, label: "Pull request" }
  d2@{ shape: diam, label: "Approved?" }
  s6@{ shape: rounded, label: "<small>Jenkins · system</small><br>Merge and publish" }
  e2@{ shape: rounded, label: "<small>Jenkins · event</small><br>Model updated" }
  s9@{ shape: fr-circ, label: " " }
  s0 --> e1 --> s1 --> s2 --> s4 --> d1
  d1 -->|no| s2
  d1 -->|yes| s5 --> d2
  s5 -.- o1
  d2 -->|changes requested| s2
  d2 -->|approved| s6 --> e2 --> s9
  class e1,e2 event
  class s1 human
  class s2 agent
  class s4,s6 system
  class s5 gate
  class d1,d2 decision
  class o1 business"""

# ---------------------------------------------------------------------------------------------------------------------
CHANGE_VIEW = """\
# views/change-the-model-diff.yaml: target compared with the baseline of PRC-04
id: VIEW-09
kind: process-change
process: PRC-04
baseline: model@a41c9e2          # the merged model the target is compared with
target: branch change/agent-drafts
renderer: plantuml
# marks are computed from the two versions, never typed:
#   added · changed · moved · removed (unchanged steps carry no mark)
"""
CHANGE_PU = """\
@startuml
!include aitoolbox.puml
title PRC-04, target compared with the baseline
|Requester|
start
AX_Event("Change requested")
AX_Step("Describe the change in chat", "human", "changed")
|Architecture agent|
AX_Step("Draft the model update", "agent", "added")
|Lead architect|
AX_Step("Update the diagram by hand", "human", "removed")
|Jenkins|
AX_Step("Validate schema and references", "system", "added")
|Lead architect|
AX_Gate("Review the pull request")
|Jenkins|
AX_Step("Notify the requester", "system", "moved")
AX_Step("Merge and publish", "system", "added")
AX_Event("Model updated")
stop
legend right
  + added   Δ changed   ↕ moved   − removed
  Steps without a mark are unchanged.
endlegend
@enduml"""
CHANGE_MM = """\
flowchart TB
  s0@{ shape: sm-circ, label: " " }
  e1@{ shape: rounded, label: "<small>Requester · event</small><br>Change requested" }
  s1@{ shape: rounded, label: "<small>Requester</small><br>Δ Describe the change in chat" }
  s2@{ shape: rounded, label: "<small>✦ Architecture agent</small><br>+ Draft the model update" }
  s3@{ shape: rounded, label: "<small>Lead architect</small><br>− <s>Update the diagram by hand</s>" }
  s4@{ shape: rounded, label: "<small>Jenkins · system</small><br>+ Validate schema and references" }
  s5@{ shape: rounded, label: "<small>Lead architect · review gate</small><br>Review the pull request" }
  s6@{ shape: rounded, label: "<small>Jenkins · system</small><br>↕ Notify the requester" }
  s7@{ shape: rounded, label: "<small>Jenkins · system</small><br>+ Merge and publish" }
  e2@{ shape: rounded, label: "<small>Jenkins · event</small><br>Model updated" }
  s9@{ shape: fr-circ, label: " " }
  s0 --> e1 --> s1 --> s2 -.-> s3 -.-> s4 --> s5 --> s6 --> s7 --> e2 --> s9
  class e1,e2 event
  class s1 changed
  class s2,s4,s7 added
  class s3 removed
  class s6 moved
  class s5 gate"""

# ---------------------------------------------------------------------------------------------------------------------
STATE_VIEW = """\
# model/data/data-objects.yaml: the life cycle is part of the object
- id: DOB-06
  type: data-object
  name: Agent output
  lifecycle:
    initial: drafted
    states: [drafted, in-review, changes-requested, approved, rejected, published, retired]
    transitions:
      - {from: drafted, to: drafted, on: checks fail, by: agent, do: fix findings}
      - {from: drafted, to: in-review, on: submitted, when: checks pass}
      - {from: in-review, to: changes-requested, on: changes requested, by: reviewer}
      - {from: changes-requested, to: drafted, on: revised, by: agent}
      - {from: in-review, to: approved, on: approved, by: reviewer}
      - {from: in-review, to: rejected, on: rejected, by: reviewer}
      - {from: approved, to: published, on: merged, do: write to the knowledge base}
      - {from: published, to: retired, on: superseded}
    final: [rejected, retired]
# views/agent-output-life-cycle.yaml
id: VIEW-10
kind: state-machine
object: DOB-06
current: in-review           # optional: an instance's state, drawn as the current state
renderer: mermaid
"""
STATE_PU = """\
@startuml
!include aitoolbox.puml
hide stereotype
hide empty description
title Agent output (DOB-06), life cycle
[*] --> Drafted : ✦ agent drafts
state "Drafted" as Drafted
state "In review" as InReview <<current>>
state "Changes requested" as Changes
state "Approved" as Approved
state "Rejected" as Rejected
state "Published" as Published
state "Retired" as Retired
Drafted --> Drafted : ✦ fix\\n[checks fail]
Drafted --> InReview : submitted\\n[checks pass]
InReview --> Changes : reviewer requests changes
Changes --> Drafted : ✦ agent revises
InReview --> Approved : reviewer approves
InReview --> Rejected : reviewer rejects
Approved --> Published : merged\\n/ write to the knowledge base
Published --> Retired : superseded
Rejected --> [*]
Retired --> [*]
@enduml"""
STATE_MM = """\
stateDiagram-v2
  [*] --> Drafted : ✦ agent drafts
  Drafted --> Drafted : ✦ fix [checks fail]
  Drafted --> InReview : submitted [checks pass]
  InReview --> Changes : reviewer requests changes
  Changes --> Drafted : ✦ agent revises
  InReview --> Approved : reviewer approves
  InReview --> Rejected : reviewer rejects
  Approved --> Published : merged / write to the knowledge base
  Published --> Retired : superseded
  Rejected --> [*]
  Retired --> [*]
  InReview : In review
  Changes : Changes requested
  class InReview current"""

# ---------------------------------------------------------------------------------------------------------------------
CLASS_VIEW = """\
# docs/detailed-design/knowledge-base.md: written with the code, rendered by the same theme
# (detailed design is not generated from the model: it refines DOB-04 and DOB-06)
kind: class
renderer: mermaid
refines: [DOB-04, DOB-06]
"""
CLASS_PU = """\
@startuml
!include aitoolbox.puml
hide circle
title Knowledge base, domain model
class ModelElement <<aggregate root>> $AX_APPLICATION_FILL;line:$AX_APPLICATION_INK;line.bold {
  id : ElementId
  type : ElementType
  name : String
  status : Status
  agent : Boolean
}
class Relation <<entity>> {
  type : RelationType
}
class ElementId <<value object>> $AX_HIGHEST;line:$AX_OUTLINE_NH {
  value : String
  {method} pattern ^[A-Z]{3}-[0-9]{2,3}$
}
class View <<entity>> {
  id : String
  kind : ViewKind
  renderer : Renderer
}
class AgentOutput <<aggregate root>> $AX_APPLICATION_FILL;line:$AX_APPLICATION_INK;line.bold {
  id : String
  status : OutputStatus
  branch : String
}
class Review <<entity>> {
  reviewer : Person
  decision : Decision
  decidedAt : Instant
}
enum Status $AX_HIGHEST;line:$AX_OUTLINE_NH {
  draft
  validated
  retired
}
ModelElement "1" *-- "0..*" Relation : from
Relation "0..*" --> "1" ModelElement : to
ModelElement --> ElementId
ModelElement ..> Status
View "0..*" o-- "1..*" ModelElement : shows
AgentOutput "1" *-- "0..*" Review
AgentOutput ..> ModelElement : proposes
@enduml"""
CLASS_MM = """\
classDiagram
  direction LR
  class ModelElement {
    <<aggregate root>>
    id : ElementId
    type : ElementType
    name : String
    status : Status
    agent : Boolean
  }
  class Relation {
    <<entity>>
    type : RelationType
  }
  class ElementId {
    <<value object>>
    value : String
  }
  class View {
    <<entity>>
    id : String
    kind : ViewKind
    renderer : Renderer
  }
  class AgentOutput {
    <<aggregate root>>
    id : String
    status : OutputStatus
    branch : String
  }
  class Review {
    <<entity>>
    reviewer : Person
    decision : Decision
    decidedAt : Instant
  }
  class Status {
    <<enumeration>>
    draft
    validated
    retired
  }
  ModelElement "1" *-- "0..*" Relation : from
  Relation "0..*" --> "1" ModelElement : to
  ModelElement --> ElementId
  ModelElement ..> Status
  View "0..*" o-- "1..*" ModelElement : shows
  AgentOutput "1" *-- "0..*" Review
  AgentOutput ..> ModelElement : proposes
  class ModelElement:::root
  class AgentOutput:::root
  class Relation:::entity
  class View:::entity
  class Review:::entity
  class ElementId:::valueobject
  class Status:::valueobject"""

# ---------------------------------------------------------------------------------------------------------------------
SEQ_VIEW = """\
# docs/detailed-design/agent-drafts-a-change.md
kind: sequence
renderer: mermaid
participants:                 # performer decides the look: person · agent · component · external
  - {id: ROL-02, as: Architect, kind: person}
  - {id: APC-01, as: Chat, kind: component}
  - {id: APC-07, as: Architecture agent, kind: agent}
  - {id: APC-02, as: Knowledge base, kind: component}
  - {as: Git hosting, kind: external}
  - {as: Jenkins, kind: external}
"""
SEQ_PU = """\
@startuml
!include aitoolbox.puml
hide stereotype
title The agent drafts a model change
actor "Architect" as U
participant "Chat" as C
participant "✦ Architecture agent" as A <<agent>>
participant "Knowledge base" as K
participant "Git hosting" as G <<external>>
participant "Jenkins" as J <<external>>
U -> C : Add a review step to PRC-04
C -> A : draft(change)
A -> K : search(PRC-04, related)
K --> A : elements, views
A -> G : branch, commit YAML, open pull request
G -> J : pull request opened
J -> J : schema and reference checks
J --> G : checks passed
A --> C : pull request #142 ready for review
C --> U : review link
alt approved
  U -> G : approve and merge
  G -> K : publish model @ sha
else changes requested
  U -> G : request changes
  G -> A : review comments
end
@enduml"""
SEQ_MM = """\
sequenceDiagram
  actor U as Architect
  participant C as Chat
  participant A as ✦ Architecture agent
  participant K as Knowledge base
  participant G as Git hosting
  participant J as Jenkins
  U->>C: Add a review step to PRC-04
  C->>A: draft(change)
  A->>K: search(PRC-04, related)
  K-->>A: elements, views
  A->>G: branch, commit YAML, open pull request
  G->>J: pull request opened
  J->>J: schema and reference checks
  J-->>G: checks passed
  A-->>C: pull request #142 ready for review
  C-->>U: review link
  alt approved
    U->>G: approve and merge
    G->>K: publish model @ sha
  else changes requested
    U->>G: request changes
    G->>A: review comments
  end"""

# ---------------------------------------------------------------------------------------------------------------------
COMP_VIEW = """\
# views/knowledge-base-components.yaml
id: VIEW-11
kind: component
renderer: plantuml
components: [APC-01, APC-07, APC-02, APC-08, APC-10]
interfaces:                                  # provided by → used by
  - {id: API-02, name: Agent API, by: APC-07, used: [APC-01]}
  - {id: API-03, name: Search API, by: APC-02, used: [APC-07]}
  - {id: API-04, name: Model API, by: APC-02, used: [APC-08, APC-10]}
external: [Git hosting, Jenkins]
"""
COMP_PU = """\
@startuml
!include aitoolbox.puml
title Knowledge base, components
component "Chat" as C
component "Architecture agent\\n<size:10>✦ agent</size>" as A
component "Knowledge base" as K
component "Model validator" as V
component "View generator" as W
component "Git hosting" as G <<external>>
component "Jenkins" as J <<external>>
interface "Agent API" as IA
interface "Search API" as IS
interface "Model API" as IM
interface "Git REST" as IG
hide stereotype
A -up- IA
K -up- IS
K -- IM
G -- IG
C ..> IA : uses
A ..> IS : uses
A ..> IG : uses
V ..> IM : uses
W ..> IM : uses
J --> V : runs on each pull request
@enduml"""
COMP_MM = """\
flowchart LR
  C["Chat"]
  A["Architecture agent<br><small>✦ agent</small>"]
  K["Knowledge base"]
  V["Model validator"]
  W["View generator"]
  G["Git hosting"]
  J["Jenkins"]
  IA@{ shape: circle, label: "Agent API" }
  IS@{ shape: circle, label: "Search API" }
  IM@{ shape: circle, label: "Model API" }
  IG@{ shape: circle, label: "Git REST" }
  A --- IA
  K --- IS
  K --- IM
  G --- IG
  C -.->|uses| IA
  A -.->|uses| IS
  A -.->|uses| IG
  V -.->|uses| IM
  W -.->|uses| IM
  J -->|runs on each pull request| V
  class C,A,K,V,W application
  class G,J external
  class IA,IS,IM,IG human"""

# ---------------------------------------------------------------------------------------------------------------------
ER_VIEW = """\
# docs/detailed-design/knowledge-base-schema.md (PostgreSQL)
kind: er
renderer: mermaid
refines: [DOB-04, DOB-06]
"""
ER_PU = """\
@startuml
!include aitoolbox.puml
hide circle
skinparam linetype ortho
title Knowledge base, tables
entity "model_element" as me {
  *id : varchar(7) <<PK>>
  --
  *type : varchar
  *name : text
  *status : varchar
  agent : boolean
}
entity "relation" as rel {
  *id : uuid <<PK>>
  --
  *type : varchar
  *from_id : varchar(7) <<FK>>
  *to_id : varchar(7) <<FK>>
}
entity "view" as v {
  *id : varchar(8) <<PK>>
  --
  *kind : varchar
  *renderer : varchar
}
entity "view_element" as ve {
  *view_id : varchar(8) <<FK>>
  *element_id : varchar(7) <<FK>>
}
entity "agent_output" as ao {
  *id : uuid <<PK>>
  --
  *status : varchar
  branch : text
}
entity "review" as rv {
  *id : uuid <<PK>>
  --
  *output_id : uuid <<FK>>
  *reviewer : text
  *decision : varchar
  decided_at : timestamptz
}
me ||--o{ rel : from
me ||--o{ rel : to
v ||--o{ ve
me ||--o{ ve
ao ||--o{ rv
@enduml"""
ER_MM = """\
erDiagram
  model_element ||--o{ relation : "from / to"
  view ||--o{ view_element : shows
  model_element ||--o{ view_element : "is shown in"
  agent_output ||--o{ review : "is reviewed by"
  model_element {
    varchar id PK
    varchar type
    text name
    varchar status
    boolean agent
  }
  relation {
    uuid id PK
    varchar type
    varchar from_id FK
    varchar to_id FK
  }
  view {
    varchar id PK
    varchar kind
    varchar renderer
  }
  view_element {
    varchar view_id FK
    varchar element_id FK
  }
  agent_output {
    uuid id PK
    varchar status
    text branch
  }
  review {
    uuid id PK
    uuid output_id FK
    text reviewer
    varchar decision
    timestamptz decided_at
  }"""


def samples():
    lp, lm, ly = gen_layered()
    return {
        "layered": (lp, lm, ly), "workflow": (WORKFLOW_PU, WORKFLOW_MM, WORKFLOW_VIEW),
        "process-change": (CHANGE_PU, CHANGE_MM, CHANGE_VIEW), "state-machine": (STATE_PU, STATE_MM, STATE_VIEW),
        "class": (CLASS_PU, CLASS_MM, CLASS_VIEW), "sequence": (SEQ_PU, SEQ_MM, SEQ_VIEW),
        "component": (COMP_PU, COMP_MM, COMP_VIEW), "er": (ER_PU, ER_MM, ER_VIEW),
    }
