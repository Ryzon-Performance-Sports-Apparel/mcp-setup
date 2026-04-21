---
description: "Dokumentiere eine Business-Entscheidung strukturiert im Decision Log mit Begründung und Kontext-Referenzen"
---

Der User hat `/decision` aufgerufen. Arguments: $ARGUMENTS

Decisions sind privilegierte Einträge — sie haben ein strengeres Schema und höhere Gewichtung (default `weight: high`).

## Dein Vorgehen

### 1. Verstehe die Frage

Der User nennt meist eine Frage oder ein Thema. Beispiel:
`/decision CRM-Tool-Wahl: HubSpot vs Pipedrive`

Extrahiere:
- **question** — die Entscheidungsfrage (aus $ARGUMENTS)
- **entities** — die betroffenen Dinge (CRM, HubSpot, Pipedrive)

### 2. Prüfe, ob bereits eine Decision existiert

**Bevor du eine neue Decision anlegst:**
1. Nutze den GitHub-Connector, um im Decision-Log-Pfad (`/entries/decisions/`) zu suchen
2. Prüfe, ob eine Decision zur selben Frage / zu denselben Entities existiert
3. Wenn ja: **zeige sie** und frage: *"Diese Decision existiert bereits. Ist die Situation neu (→ `supersedes`) oder war dir das nicht bewusst?"*

### 3. Leite das Schema durch — eine Frage nach der anderen

Frage den User in dieser Reihenfolge (immer nur 1 Frage pro Turn):

1. **"Welche Kontext-Quellen hast du für die Entscheidung genutzt?"**
   - User nennt Files, Quellen, KPIs → speichere als `context_used: [...]`
   - Wenn User nichts nennt: frage *"Keine Quellen? Reiner Bauchentscheid? → dann confidence: draft"*

2. **"Wie lautet deine Entscheidung in einem Satz?"**
   → `decision: "..."`

3. **"Begründung — warum genau so?"** (mehrere Sätze ok)
   → `rationale: "..."`

4. **"Wer hat mitentschieden?"**
   → `decided_by: [...]`

5. **"Supersedes eine frühere Decision?"** (nur falls Schritt 2 eine fand)
   → `supersedes: <id>`

### 4. Default-Felder setzen

- `type: decision`
- `domain` — aus Kontext (nachfragen wenn unklar)
- `date: <heute>`
- `decided_at: <heute>`
- `weight: high` (Decisions sind immer hoch gewichtet)
- `confidence: verified` (wenn `context_used` gefüllt) oder `draft` (wenn nicht)
- `id: dec-<YYYY-MM-DD>-<slug>`

### 5. Generiere Body

```markdown
---
type: decision
id: dec-2026-04-20-crm-tool
domain: ops
entities: [crm, hubspot, pipedrive]
date: 2026-04-20
decided_at: 2026-04-20
decided_by: [simon, mario]
confidence: verified
weight: high
context_used:
  - entries/sales/2026-04-15-analysis-crm-kpis.md
  - entries/ops/2026-04-12-meeting-tooling-review.md
question: "Welches CRM setzen wir ab Q2 ein?"
decision: "HubSpot"
rationale: "..."
tags: [crm, tooling, q2-planning]
---

# CRM-Tool-Wahl: HubSpot vs Pipedrive

## Frage
Welches CRM setzen wir ab Q2 ein?

## Entscheidung
HubSpot.

## Begründung
[rationale als lesbare Prosa, 3–5 Sätze]

## Was wir berücksichtigt haben
- [Quelle 1 mit 1-Zeilen-Kern]
- [Quelle 2 mit 1-Zeilen-Kern]

## Was sich ändern müsste, um die Decision zu überdenken
[1–2 Bedingungen — macht spätere Reviews greifbar]
```

### 6. Commit

Pfad: `/entries/decisions/<id>.md`
Commit-Message: `decision(<domain>): <question>`

### 7. Bestätige + Verweise

Antworte: *"Decision als `<id>` im Log. Sie wird ab jetzt bei ähnlichen Fragen automatisch herangezogen (weight: high). Willst du das jetzt an Sophie/Luca teilen?"*

## Wichtig

- **Keine Decision ohne rationale** — das ist der Kern des ganzen Logs
- **Wenn User ohne Kontext-Quellen entscheidet:** sage explizit *"Wir markieren das als draft — beim nächsten Review prüfen wir, ob sie verified werden kann."*
- **Niemals eine Decision überschreiben** — immer `supersedes` nutzen, alte bleibt erhalten
- **Meta-Zeile am Ende, falls Schema-Lücken:** z.B. *"📝 Feld 'impact' fehlt — wäre hilfreich für post-hoc Evaluierung"*
