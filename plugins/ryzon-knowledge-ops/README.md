# ryzon-knowledge-ops

**Claude-Plugin für Ryzon Ops & Commercial — strukturierte Wissens-Erfassung, Decision Log, transparente Retrieval.**

*v0.1 · Stand 2026-04-20 · Experiment-MVP*

---

## Was es macht

Vier Slash-Commands für das Arbeiten mit einem GitHub-basierten Knowledge-Repo:

| Command | Zweck |
|---|---|
| `/capture <type> <content>` | Neuen Wissens-Eintrag (note · learning · analysis · meeting) strukturiert anlegen |
| `/decision <question>` | Business-Entscheidung dokumentieren, mit Schema-geleiteter Befragung |
| `/pull <scope>` | Relevanten Kontext für eine Domain/Entity als Session-Start laden |
| `/sources` | Quellen der letzten Antwort detailliert auflisten |

Die Commands erwarten:
- Ein **GitHub-Repo** (default: `ryzon-knowledge-ops`) mit Struktur gemäß `docs/frontmatter-schema.md`
- Einen **Claude Project** mit **GitHub-Connector** aktiv
- **Project Instructions** aus `docs/knowledge-setup/claude-project-instructions-template.md` (im Haupt-Repo)

## Installation

### Für den Endnutzer (Sophie, Luca, Mario)

1. Claude App öffnen
2. **Customize** → **Directory** → **Plugins** → **Personal**
3. **Upload plugin** → dieses Verzeichnis als ZIP hochladen
4. Plugin aktivieren im Claude Project "Ryzon Knowledge Ops"
5. Erste Nutzung: `/pull sales` oder `/capture note ...`

### Für den Admin (Simon)

Distribution-Optionen:
- **Direct Upload:** ZIP dieses Verzeichnisses in Claude App hochladen (Personal Plugin)
- **Marketplace:** eigene Ryzon-Plugin-Marketplace auf privatem GitHub hosten, im Directory via "Add marketplace" einbinden

## Architektur-Annahmen

- **Source of Truth:** GitHub-Repo mit `.md`-Files + Frontmatter (siehe `docs/frontmatter-schema.md`)
- **Retrieval:** Tag-basierter Filter über Frontmatter + Decision-Log-Priority
- **Kein Custom MCP Server nötig im MVP** — alles läuft über den nativen GitHub-Connector der Claude App

## Was NICHT im MVP

- Context Packs (`/pack`) — ab Woche 5+
- Consistency Check (`/consistency`) — ab Woche 3+
- Firestore-Mirror — Hybrid-Phase nach Woche 6+
- Automatische Tag-Vorschläge via Embeddings — später
- Graph-Retrieval — Q3+

## Entwicklung

Wichtigste Files:
- `.claude-plugin/plugin.json` — Plugin-Manifest
- `commands/*.md` — die 4 Slash-Commands als Prompt-Files
- `docs/frontmatter-schema.md` — Schema-Spec (im Repo ebenfalls hinterlegen!)

## Change Log

- **0.1.0 (2026-04-20):** Initialer MVP mit 4 Commands für Woche 1 des Experiments
