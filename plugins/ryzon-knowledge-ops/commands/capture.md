---
description: "Lege einen strukturierten Wissens-Eintrag (note/learning/analysis/meeting) im Knowledge-Repo an"
---

Der User hat `/capture` aufgerufen. Arguments: $ARGUMENTS

## Dein Vorgehen

### 1. Parse Arguments

Der erste Token ist der **type**, der Rest ist der **content**.

Erlaubte types: `note` · `learning` · `analysis` · `meeting`

Beispiel: `/capture learning Apollo bevorzugt Video-Content über Single-Image, CTR 2x höher`
→ type=learning, content="Apollo bevorzugt..."

**Wenn type fehlt oder ungültig:** frage nach mit einem Multi-Choice: *"Welcher Typ — note, learning, analysis, oder meeting?"*

### 2. Bestimme Pflichtfelder

Schema (siehe `docs/frontmatter-schema.md` im Repo):

- `type` — aus Args
- `domain` — sales · marketing · product · ops · customer
  - Versuche aus content abzuleiten. Wenn mehrdeutig: **frage kurz nach**
- `entities` — Kunden, Projekte, Kampagnen
  - Extrahiere aus content. Schlage 2–3 vor, lass User bestätigen/ergänzen
- `date` — heutiges Datum (ISO)
- `author` — aktueller User (frage einmal am Session-Start)
- `confidence` — default `draft`. Nur `verified`, wenn User explizit sagt: *"das ist verified"*
- `weight` — default `normal`. `high` nur bei explizitem Signal ("wichtig", "zentral")
- `tags` — 2–5 Tags aus der README-Taxonomie. Wenn kein passender Tag existiert: schlage neuen vor und flagge das für Retro

### 3. Generiere Filename

Format: `<YYYY-MM-DD>-<type>-<slug>.md`
- `slug` = erste 4–6 bedeutsame Wörter des title/content, kleingeschrieben, mit Bindestrichen
- Beispiel: `2026-04-20-learning-apollo-video-content-performance.md`

### 4. Generiere Body

```markdown
---
type: learning
domain: marketing
entities: [apollo, video-content]
date: 2026-04-20
author: sophie
confidence: draft
weight: normal
tags: [performance, creative, cross-channel]
---

# Apollo: Video-Content performt 2x besser als Single-Image

Im letzten Review zeigte sich: Apollos Video-Ads hatten 2.0x CTR im
Vergleich zu Single-Image-Ads, bei vergleichbarem Spend.

[User-content hier ausformuliert — NICHT nur Copy-Paste, sondern
knapp redigiert. Max 200 Wörter. Fragen am Ende, falls offen.]
```

### 5. Schreibe ins Repo

Nutze den GitHub-Connector, um das File in den Repo-Pfad `/entries/<domain>/<filename>` zu committen.

Commit-Message: `capture(<domain>): <title>`

### 6. Bestätige

Antworte: *"Gespeichert als `<pfad>`. Zusammenfassung: <title>. Tags: [...]. Confidence: draft. Willst du etwas anpassen oder Tags nachbearbeiten?"*

Lass den User die Chance, es noch zu verfeinern, bevor wir weitergehen.

## Wichtig

- **Keine Einträge ohne Pflichtfelder** — lieber 1–2 Rückfragen als ein unvollständiger Eintrag
- **Kondensiere den Content** — User schreibt oft wie gesprochen, dein Job ist Struktur
- **Default confidence: draft** — Upgrade auf `verified` ist ein bewusster Akt, nicht Default
- **Bei Tag-Unklarheit:** schlage vor, aber merke dir in einer Meta-Zeile am Ende der Antwort: *"📝 Tag [X] fehlte in Taxonomie — für Retro notiert"*
