---
description: "Zeige die Quellen der letzten Antwort — Backup, falls der Quellen-Block übersehen wurde"
---

Der User hat `/sources` aufgerufen.

Project Instructions sollten bei jeder Antwort bereits einen Quellen-Block liefern (F4 — Context Audit). Dieser Command ist ein **Fallback** oder **Detail-Ansicht**.

## Dein Vorgehen

### 1. Schaue zurück auf deine letzte Antwort

Welche Repo-Files hast du genutzt? Wie hast du sie gewichtet?

### 2. Liefere eine detaillierte Quellen-Tabelle

```
Quellen der letzten Antwort:

| File | Confidence | Warum relevant | Einfluss |
|---|---|---|---|
| dec-2026-04-15-crm-tool.md | ✅ verified | Beantwortete die Kern-Frage direkt | ▶ maßgeblich |
| learning-apollo-ctr.md | 📝 draft | Kontext zur Apollo-Situation | mittel |
| meeting-q2-planning.md | ✅ verified | Timeline-Referenz | niedrig |

**Hinweis:** 1 Eintrag war `draft` — die Information ist noch nicht verified.
Willst du die Antwort mit `/only-verified` noch einmal generieren?
```

### 3. Falls keine Repo-Quellen genutzt

Wenn die letzte Antwort rein auf Allgemeinwissen basierte:

```
Quellen: keine Repo-Inhalte.

Die letzte Antwort basierte auf Allgemeinwissen (nicht Ryzon-spezifisch).
Wenn es einen Repo-Eintrag dazu gibt, hätte ich ihn nutzen sollen.
Soll ich noch einmal prüfen, ob es relevante Einträge gibt?
```

### 4. Falls die letzte Antwort unsicher war

Wenn du in der letzten Antwort markiert hattest *"ich bin mir bei X nicht sicher"*: wiederhole das hier und schlage `/capture` vor, um die Info einzutragen, sobald sie geklärt ist.

## Wichtig

- **Lüge nicht über Quellen** — wenn du aus Versehen einen Eintrag falsch zugeordnet hast in der vorherigen Antwort, korrigiere es jetzt ehrlich
- **Wenn unklar, welche Files genutzt wurden:** sag es: *"Ich bin mir nicht sicher, welche Files die Antwort im Detail geprägt haben. Lass mich die Antwort noch einmal mit expliziter Retrieval-Spur generieren — willst du das?"*
