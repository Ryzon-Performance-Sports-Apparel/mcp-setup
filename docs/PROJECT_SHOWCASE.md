# Ryzon AI Platform — Project Overview

> Alle Unternehmensdaten an einem Ort — als Fundament für AI-Agenten, LLM-Anwendungen und smarte Cloud-Services.

---

## Die Vision

Unternehmenswissen ist heute über Dutzende Tools verstreut: Meeting-Notizen in Google Drive, Aufgaben in Asana, Kreativ-Assets in Figma, Kundendaten im ERP, E-Mails in Gmail. Jedes Tool hat seine eigene Suche, sein eigenes Format, seinen eigenen Zugang.

**Die zentrale Datenbank ändert das.** Sie sammelt Informationen aus allen Quellen, reichert sie mit AI an und stellt sie einheitlich bereit — für AI-Agenten, für LLM-Anwendungen via MCP, und für Web-Services in der Cloud.

```
Team-Mitglied:  "Was wurde in den letzten Meetings zum Thema ERP beschlossen?"

AI-Agent:       Ich habe 4 relevante Meetings gefunden:
                - 18.03. ERP-Auswahl: Shortlist auf Odoo und NetSuite eingegrenzt
                - 25.03. Vendor-Demo: Odoo überzeugt bei Warenwirtschaft
                - 01.04. Entscheidung: Odoo wird Pilotprojekt ab Mai
                - 07.04. Kick-off: Simon koordiniert Implementierung
```

---

## Die Architektur — Zentrale Datenbank als Fundament

```mermaid
graph TB
    subgraph "Datenquellen — alles fließt rein"
        DRIVE["Google Drive\n(Meeting-Notizen,\nDokumente)"]
        ASANA["Asana\n(Aufgaben,\nProjekte)"]
        ERP["ERP-System\n(Kunden, Bestellungen,\nWarenwirtschaft)"]
        EMAIL["E-Mail\n(Gmail, Outlook)"]
        FIGMA["Figma\n(Designs,\nCreatives)"]
        GRANOLA["Granola.ai\n(AI Meeting Notes)"]
    end

    subgraph "Sync-Pipelines — automatisch, stündlich"
        SYNC["Sync-Engine\n+ AI-Anreicherung"]
    end

    subgraph "ZENTRALE DATENBANK"
        direction TB
        FS["Firestore Knowledge Base"]
        GCS["Cloud Storage\n(Dateien & Bilder)"]

        FS --- |"Texte, Metadaten,\nVektoren, Tags"| DB_NOTE["Meeting Notes"]
        FS --- |"Aufgaben,\nDeadlines"| DB_TASK["Projektdaten"]
        FS --- |"Kunden,\nBestellungen"| DB_ERP["ERP-Daten"]
        FS --- |"Korrespondenz,\nAnhänge"| DB_EMAIL["E-Mails"]
    end

    subgraph "Verbraucher — alles greift darauf zu"
        MCP["AI-Agenten\nvia MCP"]
        WEB["Web-Apps\nin der Cloud"]
        LLM["LLM-Anwendungen\n(Claude, GPT, etc.)"]
        DASH["Dashboards\n& Reports"]
    end

    DRIVE --> SYNC
    ASANA --> SYNC
    ERP --> SYNC
    EMAIL --> SYNC
    FIGMA --> SYNC
    GRANOLA --> SYNC

    SYNC --> FS
    SYNC --> GCS

    FS --> MCP
    FS --> WEB
    FS --> LLM
    FS --> DASH
    GCS --> MCP
    GCS --> WEB

    style FS fill:#FF6F00,color:#fff,stroke:#FF6F00,stroke-width:3px
    style GCS fill:#4285F4,color:#fff
    style SYNC fill:#10B981,color:#fff
    style MCP fill:#8B5CF6,color:#fff
    style WEB fill:#3B82F6,color:#fff
    style LLM fill:#8B5CF6,color:#fff
    style DASH fill:#3B82F6,color:#fff
```

### Warum eine zentrale Datenbank?

| Ohne zentrale DB | Mit zentraler DB |
|-----------------|-----------------|
| Jedes Tool hat eigene Suche | **Eine Suche** findet alles |
| AI kann nur ein Tool gleichzeitig nutzen | AI hat **Zugriff auf alles** in einem Schritt |
| Web-Apps brauchen je eine eigene Integration | Web-Apps nutzen **eine einzige Quelle** |
| Wissen geht verloren | Alles wird **dauerhaft gespeichert und angereichert** |
| Kontextwechsel für jede Frage | **Ein Ort** für alle Fragen |

---

## Wie Daten in die zentrale Datenbank kommen

```mermaid
sequenceDiagram
    participant Quelle as Datenquelle
    participant Sync as Sync-Pipeline
    participant AI as AI-Anreicherung
    participant DB as Zentrale Datenbank
    participant Agent as AI-Agent / Web-App

    Quelle->>Sync: Neue Daten verfügbar
    Sync->>Sync: Abholen & Formatieren
    Sync->>DB: Rohdaten speichern

    Note over AI,DB: Automatisch bei jedem neuen Dokument

    DB->>AI: Neues Dokument eingetroffen
    AI->>AI: Zusammenfassung erstellen
    AI->>AI: Tags & Kategorien vergeben
    AI->>AI: Aktionspunkte extrahieren
    AI->>AI: Sprache erkennen
    AI->>AI: Datenschutz-Check (PII)
    AI->>AI: Semantischen Vektor erzeugen
    AI->>DB: Angereichertes Dokument speichern

    Agent->>DB: "Was wissen wir über Thema X?"
    DB->>Agent: Relevante Dokumente + Zusammenfassungen
```

### Was die AI aus jedem Dokument extrahiert

| Feld | Beispiel |
|------|---------|
| **Zusammenfassung** | "Team hat Q2-Roadmap besprochen, Fokus auf Mobile-First" |
| **Tags** | `q2-roadmap`, `mobile`, `produkt-strategie` |
| **Aktionspunkte** | "Simon erstellt Mobile-Spec bis 14. April" |
| **Entscheidungen** | "Mobile-First für Q2", "Desktop-Redesign verschoben" |
| **Kategorie** | Planning, Standup, Review, Retro, 1:1, Demo, etc. |
| **Sprache** | Deutsch, Englisch, etc. |
| **Datenschutz** | Sicher oder Enthält personenbezogene Daten |
| **Semantischer Vektor** | Ermöglicht Suche nach Bedeutung, nicht nur nach Stichworten |

---

## Wer nutzt die zentrale Datenbank?

```mermaid
graph TB
    subgraph "Zentrale Datenbank"
        DB["Firestore\nKnowledge Base"]
    end

    subgraph "AI-Agenten via MCP"
        A1["Meta Ads Agent\nErstellt Kampagnen mit\nWissen über Produkte & Assets"]
        A2["Google Ads Agent\nOptimiert Anzeigen basierend\nauf Meeting-Entscheidungen"]
        A3["Recherche-Agent\nBeantwortet Fragen aus\nallen Quellen gleichzeitig"]
        A4["Reporting-Agent\nErstellt Berichte aus\nERP + Meetings + Tasks"]
    end

    subgraph "Web-Anwendungen"
        W1["Internes Dashboard\nTeam-Wissen auf\neinen Blick"]
        W2["Kunden-Portal\nRelevante Infos\nautomatisch bereitgestellt"]
        W3["Automatisierungen\nWorkflows basierend\nauf Datenänderungen"]
    end

    subgraph "LLM-Anwendungen"
        L1["Chat-Interface\nMitarbeiter fragen\ndirekt die Wissensbasis"]
        L2["Zusammenfassungen\nAutomatische Briefings\nfür Führungskräfte"]
        L3["Übersetzungen\nMeeting-Notizen in\nandere Sprachen"]
    end

    DB --> A1
    DB --> A2
    DB --> A3
    DB --> A4
    DB --> W1
    DB --> W2
    DB --> W3
    DB --> L1
    DB --> L2
    DB --> L3

    style DB fill:#FF6F00,color:#fff,stroke:#FF6F00,stroke-width:3px
    style A1 fill:#8B5CF6,color:#fff
    style A2 fill:#8B5CF6,color:#fff
    style A3 fill:#8B5CF6,color:#fff
    style A4 fill:#8B5CF6,color:#fff
    style W1 fill:#3B82F6,color:#fff
    style W2 fill:#3B82F6,color:#fff
    style W3 fill:#3B82F6,color:#fff
    style L1 fill:#7C3AED,color:#fff
    style L2 fill:#7C3AED,color:#fff
    style L3 fill:#7C3AED,color:#fff
```

**Der entscheidende Punkt:** Die zentrale Datenbank ist kein Tool für sich — sie ist das **Fundament**, auf dem beliebig viele AI- und Web-Anwendungen aufgebaut werden können. Jede neue Quelle, die angebunden wird, macht _alle_ Anwendungen gleichzeitig schlauer.

---

## Zwei Arten der Suche

```mermaid
graph LR
    subgraph "Tag-basierte Suche"
        Q1["Zeige alle Planning-Meetings\nzum Thema ERP\naus dem März"]
        R1["Exakte Treffer\nbasierend auf Tags,\nDatum, Kategorie"]
    end

    subgraph "Semantische Suche (AI)"
        Q2["Was wissen wir über\ndie Kundeneinrichtung?"]
        R2["Findet relevante Dokumente\nauch wenn andere Begriffe\nverwendet wurden"]
    end

    Q1 --> R1
    Q2 --> R2

    style Q1 fill:#3B82F6,color:#fff
    style Q2 fill:#8B5CF6,color:#fff
    style R1 fill:#E5E7EB,color:#000
    style R2 fill:#E5E7EB,color:#000
```

**Tag-basiert:** Schnell und präzise — "Alle Meetings mit Tag `erp-auswahl` vom März"

**Semantisch:** AI-gestützt — "Was wurde zum Thema Kundenbetreuung besprochen?" findet auch Notizen, die von "Kundensupport", "After-Sales" oder "Nachbetreuung" sprechen.

---

## Die drei MCP-Server — Brücken zwischen AI und Tools

```mermaid
graph TB
    subgraph "AI-Ebene"
        Claude["Claude AI"]
    end

    subgraph "MCP-Server"
        META["Meta Ads\n36 Tools"]
        GADS["Google Ads\n10+ Tools"]
        DAM["Digital Asset Manager\n12 Tools"]
    end

    subgraph "Zentrale Datenbank"
        DB["Firestore + Cloud Storage"]
    end

    subgraph "Externe Plattformen"
        FB["Facebook / Instagram"]
        GOOGLE["Google Ads"]
    end

    Claude -->|"Kampagnen verwalten"| META
    Claude -->|"Anzeigen verwalten"| GADS
    Claude -->|"Assets & Wissen\nsuchen und abrufen"| DAM

    META -->|"erstellt & bearbeitet"| FB
    GADS -->|"erstellt & bearbeitet"| GOOGLE
    DAM <-->|"liest & schreibt"| DB

    META -.->|"nutzt Assets aus"| DB
    GADS -.->|"nutzt Assets aus"| DB

    style Claude fill:#8B5CF6,color:#fff
    style META fill:#1877F2,color:#fff
    style GADS fill:#4285F4,color:#fff
    style DAM fill:#10B981,color:#fff
    style DB fill:#FF6F00,color:#fff,stroke:#FF6F00,stroke-width:3px
```

### Meta Ads Server — 36 Tools

> Alles für Facebook- und Instagram-Werbung: Kampagnen erstellen, Zielgruppen definieren, Performance analysieren.

- Kampagnen erstellen, bearbeiten, pausieren, duplizieren
- Alle Kreativformate: Einzelbild, Karussell, Video, Dynamic Ads
- Zielgruppen: Interessen, Verhalten, Demografie, Lookalikes
- Performance: Ausgaben, Impressions, Klicks, Conversions, ROAS

### Google Ads Server — 10+ Tools

> Google Search und Display Advertising per Sprache steuern.

- Kampagnen- und Anzeigengruppen-Management
- Keyword- und Zielgruppen-Targeting
- Performance-Reporting

### Digital Asset Manager — 12 Tools

> Kreativ-Assets und Unternehmenswissen verwalten und durchsuchen.

**Asset-Tools:**
| Tool | Was es macht |
|------|-------------|
| `list_assets` | Assets nach Kampagne durchsuchen |
| `search_assets` | Nach Name, Tags, Format oder Maßen suchen |
| `get_asset_download_url` | Sicheren Download-Link generieren |
| `upload_asset` | Neue Datei hochladen |
| `tag_asset` | Tags und Metadaten aktualisieren |
| `export_figma_frames` | Figma-Designs direkt ins DAM exportieren |

**Wissens-Tools:**
| Tool | Was es macht |
|------|-------------|
| `query_knowledge_base` | Nach Tags, Datum, Serie oder Typ suchen |
| `get_document` | Vollständiges Dokument abrufen |
| `search_knowledge_base_semantic` | Natürlichsprachliche Suche (AI-gestützt) |

---

## Datenschutz & Sicherheit

```mermaid
graph TB
    subgraph "Allgemeiner Zugang"
        KB["Knowledge Base\n(geprüfte Dokumente)"]
    end

    subgraph "Eingeschränkter Zugang"
        KBR["Geschützte Sammlung\n(personenbezogene Daten)"]
    end

    DOC["Neues Dokument"] --> AI["AI Datenschutz-Check"]
    AI -->|"Keine persönlichen Daten"| KB
    AI -->|"Enthält persönliche Daten\n(Gehalt, Gesundheit, etc.)"| KBR

    style KB fill:#10B981,color:#fff
    style KBR fill:#EF4444,color:#fff
    style AI fill:#8B5CF6,color:#fff
```

- AI prüft **jedes Dokument** automatisch auf personenbezogene Daten
- Sensible Dokumente werden in eine **geschützte Sammlung** verschoben
- Geschäftliche E-Mails und Namen im beruflichen Kontext werden **nicht** markiert
- Verschiedene **Zugriffsebenen** pro Sammlung möglich
- Alle Daten bleiben in der **EU** (Region europe-west3, Frankfurt)

---

## So funktioniert das Onboarding

### Für Team-Mitglieder (Meeting-Notizen)

```mermaid
graph LR
    S1["1. Ordner freigeben\nfür Service-Account"] --> S2["2. Zeile in\nConfig-Sheet eintragen"] --> S3["3. Fertig!\nNotizen synchen\nautomatisch"]

    style S1 fill:#3B82F6,color:#fff
    style S2 fill:#3B82F6,color:#fff
    style S3 fill:#10B981,color:#fff
```

### Für Designer

```mermaid
graph LR
    D1["Weiter wie bisher\nin Figma und Drive\narbeiten"] --> D2["Sync holt neue\nDateien automatisch\njede Stunde"] --> D3["AI kann Assets\nin Anzeigen\nverwenden"]

    style D1 fill:#F24E1E,color:#fff
    style D2 fill:#10B981,color:#fff
    style D3 fill:#8B5CF6,color:#fff
```

**Kein Workflow ändert sich.** Die Plattform arbeitet im Hintergrund.

---

## Infrastruktur

```mermaid
graph TB
    subgraph "Google Cloud Platform — Frankfurt (europe-west3)"
        subgraph "Dauerhaft aktiv"
            CR["Cloud Run\nDAM-Server"]
        end

        subgraph "Stündlich geplant"
            CF1["Meeting-Sync"]
            CF2["Asset-Sync"]
        end

        subgraph "Event-gesteuert"
            CF3["Dokument-Prozessor\n(AI-Anreicherung)"]
        end

        subgraph "Zentrale Datenbank"
            FS["Firestore"]
            GCS["Cloud Storage"]
        end
    end

    subgraph "Externe Dienste"
        CLAUDE_API["Claude AI"]
        VOYAGE["Voyage AI\n(Vektoren)"]
        META_API["Meta API"]
        DRIVE_API["Google Drive"]
    end

    CF1 --> FS
    CF2 --> GCS
    CF3 --> FS
    CF3 --> CLAUDE_API
    CF3 --> VOYAGE
    CR --> FS
    CR --> GCS

    style FS fill:#FF6F00,color:#fff,stroke:#FF6F00,stroke-width:3px
    style GCS fill:#4285F4,color:#fff
    style CR fill:#4285F4,color:#fff
    style CF1 fill:#34A853,color:#fff
    style CF2 fill:#34A853,color:#fff
    style CF3 fill:#FBBC04,color:#000
```

**Kosten:** Minimal. Cloud Functions zahlen nur bei Nutzung. Firestore und Cloud Storage kosten Cent pro Monat. AI-Verarbeitung kostet ca. 0,001 EUR pro Dokument.

---

## Roadmap

```mermaid
graph LR
    subgraph "Erledigt"
        P1["Phase 1\nAsset-Management\nDrive-Sync, Figma-Export"]
        P2["Phase 2\nAI-Anreicherung\nLLM-Tags, Vektorsuche,\nPII-Erkennung"]
    end

    subgraph "Geplant"
        P3["Phase 3\nMehr Quellen\nGranola, Asana,\nERP, E-Mail"]
        P4["Phase 4\nWorkflows\nGenehmigungen,\nWissens-Graph"]
    end

    P1 --> P2 --> P3 --> P4

    style P1 fill:#10B981,color:#fff
    style P2 fill:#10B981,color:#fff
    style P3 fill:#3B82F6,color:#fff
    style P4 fill:#3B82F6,color:#fff
```

| Phase | Status | Was kommt dazu |
|-------|--------|---------------|
| **Phase 1** — Asset-Management | Fertig | Drive-Sync, Asset-Suche, Figma-Export |
| **Phase 2** — AI-Anreicherung | Fertig | LLM-Tagging, Zusammenfassungen, Vektorsuche, PII-Erkennung |
| **Phase 3** — Weitere Quellen | Geplant | Granola.ai, Asana, ERP-Daten, E-Mails |
| **Phase 4** — Workflows & Graph | Geplant | Genehmigungen, Versionierung, Wissens-Graph über alle Quellen |

---

## Zusammenfassung

```mermaid
graph TB
    subgraph "Viele Quellen"
        S1["Drive"]
        S2["Asana"]
        S3["ERP"]
        S4["E-Mail"]
        S5["Figma"]
        S6["Granola"]
    end

    subgraph "Eine Datenbank"
        DB["Zentrale\nKnowledge Base"]
    end

    subgraph "Viele Anwendungen"
        A1["AI-Agenten"]
        A2["Web-Apps"]
        A3["LLM-Chat"]
        A4["Dashboards"]
        A5["Automatisierungen"]
    end

    S1 --> DB
    S2 --> DB
    S3 --> DB
    S4 --> DB
    S5 --> DB
    S6 --> DB

    DB --> A1
    DB --> A2
    DB --> A3
    DB --> A4
    DB --> A5

    style DB fill:#FF6F00,color:#fff,stroke:#FF6F00,stroke-width:4px
```

**Viele Quellen rein. Eine Datenbank. Viele Anwendungen raus.**

Das ist das Fundament. Jede neue Quelle macht alle Anwendungen schlauer. Jede neue Anwendung hat sofort Zugriff auf alles.

---

*Gebaut vom Ryzon-Team. Angetrieben von Claude, Meta APIs, Google APIs, Figma und einer Menge Automatisierung.*
