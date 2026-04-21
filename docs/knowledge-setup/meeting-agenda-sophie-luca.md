# Knowledge Setup — Meeting Sophie & Luca

*30 Min · Diagramm-basiert · 5 Diskussions-Punkte*

---

## Das ganze Setup auf einen Blick

```mermaid
flowchart TB
    U["👤 Sophie · Luca · Simon"]

    subgraph CP["🤖 Claude Project · Ryzon Knowledge Ops"]
        CMD["Commands: <b>/capture · /decision · /pull · /sources · /promote</b>"]
        AUD["❷ Jede Antwort: Quellen-Block + Trust-Level<br/>(verified · draft · raw)"]
    end

    subgraph WORLDS["💻 ~/Documents/projects/context/ · auf eurem Laptop"]
        direction LR

        subgraph OPV["🟡 OPERATIV<br/>ryzon-context-vault (Obsidian)"]
            OPG["granola/<br/><i>Meetings auto-synced</i>"]
            OPP["simon/ · sophie/ · luca/<br/><i>persönliche Notes</i>"]
            OPS["shared/<br/><i>Team-Scratchpad</i>"]
        end

        subgraph STR["🟢 STRATEGISCH<br/>ai-context (kuratiert)"]
            STM["meetings/<br/>promovierte Protokolle"]
            STD["decisions/<br/><b>Decision Log ❶</b>"]
            STO["domain/<br/>Team-Standards"]
        end

        subgraph PRIV["🔒 private/ · nie committed"]
            PP["1on1s · HR · Gesundheit ❺"]
        end
    end

    U ==> CP
    CP -->|"/capture · /pull"| OPV
    CP -->|"/pull · /sources"| STR
    OPV ==>|"⏳ FRIDAY RITUAL ❸<br/>Simon moderiert · 45 Min<br/>gemeinsam promote · keep · delete"| STR

    classDef userNode fill:#e8f0ff,stroke:#3050a0,stroke-width:2px,color:#000
    classDef projNode fill:#f0f4ff,stroke:#5070c0,stroke-width:2px,color:#000
    classDef opNode fill:#fff6d9,stroke:#d4a800,stroke-width:2px,color:#000
    classDef stNode fill:#d9f0d9,stroke:#2d7a2d,stroke-width:2px,color:#000
    classDef privNode fill:#ffe0e0,stroke:#cc0000,stroke-dasharray:5 5,color:#000

    class U userNode
    class CP,CMD,AUD projNode
    class OPV,OPG,OPP,OPS opNode
    class STR,STM,STD,STO stNode
    class PRIV,PP privNode
```

---

## Was ihr tut — täglich & wöchentlich

```mermaid
flowchart LR
    A["🌅 Morgens<br/>/pull sales"] --> B["✍️ Arbeiten<br/>mit Claude"]
    B --> C["💡 Insight?<br/>/capture"]
    B --> D["🎯 Entscheidung?<br/>/decision"]
    C --> E["🔍 /sources<br/>prüfen"]
    D --> E
    E --> F["⏳ Freitag<br/>/promote<br/>Ritual"]
    F --> G["✅ strategisch<br/>im Team-Standard"]

    classDef day fill:#fff6d9,stroke:#d4a800,color:#000
    classDef check fill:#e8f0ff,stroke:#3050a0,color:#000
    classDef week fill:#d9f0d9,stroke:#2d7a2d,color:#000

    class A,B,C,D day
    class E check
    class F,G week
```

---

## Diskussions-Punkte · was wir heute von euch brauchen

| | Frage | Kontext |
|---|---|---|
| **❶** | **Decision-Log-Schema — passen die Felder?** | `question · decision · rationale · context_used · decided_by · supersedes` · fehlt etwas · ist eines überflüssig? |
| **❷** | **Transparenz-Block — wie viel Detail?** | Claude listet bei jeder Antwort die Quellen · soll das sichtbar bleiben oder nur bei Bedarf (`/sources`)? |
| **❸** | **Promotion-Flow — wer entscheidet was strategisch wird?** | Freitag-Ritual: jede:r selbst · Peer-Check · Simon als Gatekeeper? |
| **❹** | **Tag-Taxonomie — frei oder kontrolliert?** | Feste Tag-Liste mit Retro-Änderungen · oder freies Tagging mit Agent-Normalisierung? |
| **❺** | **Mario ab Woche 3 — was darf er sehen?** | alles team-shared · oder bestimmte Kategorien (HR, Personalentscheidungen) weiterhin geschützt? |

---

## Timeline

```mermaid
gantt
    title 2-Wochen-Experiment + Mario-Onboarding
    dateFormat YYYY-MM-DD
    axisFormat %d.%m

    section Woche 1
    Install-Session (30 Min/Person)    :milestone, m1, 2026-04-22, 0d
    Tägliche Nutzung                   :active, 2026-04-22, 5d
    Mittwoch Check-In (30 Min)         :milestone, m2, 2026-04-24, 0d
    Ziel ≥10 Einträge pro Person       :crit, 2026-04-22, 5d
    Freitag-Ritual (45 Min)            :milestone, m3, 2026-04-26, 0d

    section Woche 2
    Cross-Reads aktivieren             :active, 2026-04-27, 5d
    Ziel ≥15 Einträge + ≥5 Cross-Refs  :crit, 2026-04-27, 5d
    Trust-Battery-Check                :milestone, m4, 2026-05-03, 0d
    Entscheidung A · B · C             :milestone, m5, 2026-05-03, 0d

    section Woche 3+
    Mario onboarding                   :milestone, m6, 2026-05-06, 0d
    Externer Berater (Phase 4)         :2026-05-13, 14d
```

---

## Was wir heute NICHT lösen

`Marios Bierdeckel` · `Semantic Search` · `KI-Auto-Tagging` · `Ryzon Cockpit` · `Externer Berater`

→ alles in Parking Lot, kommt zurück, wenn Fundament steht.
