# Frontmatter-Schema für Knowledge-Einträge

*v0.1 — Woche 1 des Experiments*

Jede `.md`-Datei im Repo beginnt mit YAML-Frontmatter. Die folgenden Felder sind **Pflicht** für alle Einträge, plus zusätzliche Felder für Decisions.

---

## Pflichtfelder (alle Typen)

| Feld | Typ | Werte | Beispiel |
|---|---|---|---|
| `type` | enum | `note` \| `meeting` \| `learning` \| `analysis` \| `decision` | `learning` |
| `domain` | enum | `sales` \| `marketing` \| `product` \| `ops` \| `customer` | `sales` |
| `entities` | array | Freie Strings, lowercase-kebab — Kunden, Projekte, Kampagnen | `[apollo, q2-campaign]` |
| `date` | ISO-Date | YYYY-MM-DD | `2026-04-20` |
| `author` | enum | `sophie` \| `luca` \| `simon` \| `mario` | `sophie` |
| `confidence` | enum | `verified` \| `draft` \| `raw` | `draft` |
| `weight` | enum | `low` \| `normal` \| `high` | `normal` |
| `tags` | array | 2–5 Tags aus Taxonomie (siehe README) | `[performance, creative]` |

---

## Zusätzliche Pflichtfelder für `type: decision`

| Feld | Typ | Pflicht | Beispiel |
|---|---|---|---|
| `id` | string | ja | `dec-2026-04-20-crm-tool` |
| `question` | string | ja | `"Welches CRM setzen wir ab Q2 ein?"` |
| `decision` | string | ja | `"HubSpot"` |
| `rationale` | string | ja (multiline) | `"..."` |
| `decided_by` | array | ja | `[simon, mario]` |
| `decided_at` | ISO-Date | ja | `2026-04-20` |
| `context_used` | array (paths) | empfohlen | `[entries/sales/...]` |
| `supersedes` | string (id) | optional | `dec-2025-11-02-crm-eval` |

**Default für Decisions:** `weight: high`, `confidence: verified` (wenn `context_used` gefüllt)

---

## Tag-Taxonomie v0.1

Tags dürfen aus dieser Liste gewählt werden. Neue Tags → im Retro besprechen, nicht freihändig einführen.

### Funktionale Tags
- `performance` — Zahlen, KPIs, ROAS, Conversion
- `creative` — Ads, Visuals, Copy
- `process` — Prozesse, Workflows, Abläufe
- `tooling` — Software-Entscheidungen, Stacks
- `customer` — direkte Kunden-Insights

### Zeitliche Tags
- `q1-planning`, `q2-planning`, `q3-planning`, `q4-planning`
- `bfcm` — Black-Friday / Cyber-Monday
- `season-spring`, `season-summer`, etc.

### Thematische Tags
- `pricing` — Preisentscheidungen, -analysen
- `launch` — Produkt-Launches
- `crm`, `hubspot`, `pipedrive`
- `apollo`, `keyaccount-<name>`

### Meta-Tags
- `needs-review` — geflaggt für Retro
- `contested` — mehrere Leute haben verschiedene Meinungen
- `hypothesis` — These, nicht verifiziert

---

## File-Naming-Convention

Pfad-Struktur:
```
entries/
├── sales/
├── marketing/
├── product/
├── ops/
├── customer/
└── decisions/    # ALLE Decisions hier, unabhängig von domain
```

Dateiname: `<YYYY-MM-DD>-<type>-<slug>.md`

Beispiele:
- `entries/sales/2026-04-20-learning-apollo-video-performance.md`
- `entries/decisions/dec-2026-04-20-crm-tool.md`
- `entries/ops/2026-04-15-meeting-tooling-review.md`

Für Decisions: Dateiname = `<id>.md`

---

## Beispiel: Learning

```markdown
---
type: learning
domain: marketing
entities: [apollo, video-content]
date: 2026-04-20
author: sophie
confidence: draft
weight: normal
tags: [performance, creative]
---

# Apollo: Video-Content performt 2x besser als Single-Image

Im Review vom 18.04. zeigte sich deutlich: Apollos Video-Ads erzielten
im März 2.0x CTR im Vergleich zu Single-Image-Ads bei vergleichbarem Spend.

Zu prüfen: ob das über weitere Kunden konsistent ist oder Apollo-spezifisch.
```

---

## Beispiel: Decision

```markdown
---
type: decision
id: dec-2026-04-20-crm-tool
domain: ops
entities: [crm, hubspot, pipedrive]
date: 2026-04-20
decided_at: 2026-04-20
decided_by: [simon, mario]
author: simon
confidence: verified
weight: high
context_used:
  - entries/sales/2026-04-15-analysis-crm-kpis.md
  - entries/ops/2026-04-12-meeting-tooling-review.md
question: "Welches CRM setzen wir ab Q2 ein?"
decision: "HubSpot"
rationale: |
  HubSpot hat bessere Integration zu unserem Marketing-Stack (Klaviyo,
  Meta Ads). Pipedrive ist zwar günstiger, aber die manuelle Daten-Pflege
  würde die Ersparnis auffressen. HubSpot-Testphase im März war
  reibungslos. Entscheidung getragen von Sales-Team.
tags: [crm, tooling, q2-planning]
---

# CRM-Tool-Wahl: HubSpot vs Pipedrive

## Frage
Welches CRM setzen wir ab Q2 ein?

## Entscheidung
HubSpot.

## Begründung
(siehe rationale)

## Was wir berücksichtigt haben
- Sales-KPI-Analyse März: Pipeline-Bearbeitung braucht Tool-Support
- Team-Feedback: 4/5 im Sales-Team präferieren HubSpot-UI

## Was sich ändern müsste, um die Decision zu überdenken
- HubSpot-Preis steigt um >30% (Re-Evaluation triggered)
- Marketing-Stack wechselt weg von Klaviyo
```

---

## Anpassungen nach Retro

Nach Friday-Retro: Änderungen hier dokumentieren mit Datum und Grund. Kein Freihand-Editing in produktiven Repos.

### Change Log
- **2026-04-20, v0.1:** Initiales Schema
