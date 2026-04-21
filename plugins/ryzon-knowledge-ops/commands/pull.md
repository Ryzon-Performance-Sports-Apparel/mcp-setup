---
description: "Lade relevanten Kontext für eine Domain oder Entity als Start-Kontext für den Chat"
---

Der User hat `/pull` aufgerufen. Arguments: $ARGUMENTS

Dieser Command lädt gezielt Kontext aus dem Repo — damit der User mit vollem Kontext in eine Aufgabe startet, statt Claude reaktiv alles einzeln ziehen zu lassen.

## Dein Vorgehen

### 1. Parse Arguments

Format: `/pull <scope>` wobei `<scope>` sein kann:
- Eine **domain**: `sales`, `marketing`, `product`, `ops`, `customer`
- Eine **entity**: `apollo`, `q2-campaign`, `hubspot`
- Ein **type-Filter**: `decisions`, `recent-learnings`
- Eine **Kombination**: `sales apollo decisions`

Beispiel: `/pull sales apollo`
→ lade alle Einträge wo domain=sales UND entities enthält "apollo"

### 2. Filter-Strategie

**Priorität beim Laden:**
1. Alle Decisions mit `weight: high` zum Scope → immer dabei
2. Einträge mit `confidence: verified` zuerst
3. Neueste 10 `confidence: draft` Einträge zum Scope
4. `confidence: raw` nur wenn User explizit sagt "mit raw"

### 3. Via GitHub-Connector holen

Nutze den GitHub-Connector:
1. Liste Files unter `/entries/` mit passendem Pfad-Präfix
2. Lies Frontmatter jedes Files
3. Filtere nach Scope
4. Lade die vollen Files der Top-Matches (max 20 Files, damit Context-Window nicht überlastet)

### 4. Gib Overview zurück

Antworte mit einer strukturierten Übersicht:

```
📥 Kontext geladen für: <scope>

**Decisions (weight: high):** 3
- dec-2026-04-15-crm-tool — "HubSpot ab Q2"
- dec-2026-03-22-sales-process — "2-stufiger Discovery-Call"
- ...

**Verified Notes / Learnings:** 5
- ...

**Recent Drafts (last 7 days):** 4
- ...

Total: 12 Files, ~8.4k Tokens.

Ich habe jetzt den Kontext im Arbeitsspeicher. Womit willst du starten?
Typische nächste Schritte:
- "Fass die wichtigsten Learnings für mich zusammen"
- "Welche offenen Fragen / Widersprüche siehst du?"
- "Bereite mich auf das nächste Apollo-Meeting vor"
```

### 5. Trust-Level sichtbar machen

Bei jedem aufgelisteten File, zeige das confidence-Level farblich oder mit Symbol:
- ✅ verified
- 📝 draft
- ⚠️ raw

## Wichtig

- **Nicht mehr als 20 Files auf einmal laden** — sonst Token-Budget weg
- **Bei zu wenig Matches** (<3): sage es ehrlich, schlage vor, den Scope zu erweitern
- **Bei zu vielen Matches** (>30): lade Top-20, sage: *"Es gibt 47 Treffer. Ich habe die Top-20 geladen. Willst du enger filtern?"*
- **Decisions mit weight: high** immer dabei, auch wenn sie strenggenommen nicht zum Scope passen — sie sind Referenz-Punkte
