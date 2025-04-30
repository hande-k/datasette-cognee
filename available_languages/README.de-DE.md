# datasette-cognee

## Einführung

Dies ist ein Plugin für Datasette, das mit cognee integriert wird, um Wissensgraphen für Datasette-Datenbanken bereitzustellen.

cognee ermöglicht es, strukturierte Daten aus SQLite-Datenbanken in ein Wissensdiagramm zu integrieren und semantische Abfragen gegen dieses Diagramm durchzuführen.

## Projekt, um Projektteilnehmer zu entdecken

Dieses Projekt nutzt https://github.com/dogsheep/github-to-sqlite um GitHub Daten in die SQLite-Datenbank zu holen, die in den Cogne migriert wird.

Als Standarddatenbank wird https://github.com/dogsheep/github-to-sqlite?tab=readme-ov-file#fetching-contributors-to-a-repository verwendet, um Mitwirkende von cogney zu holen.

```
github-to-sqlite contributors github.db topoteretes/cognee
```

Führen Sie folgendes für einen Schnelltest durch:

#### 1- Klone diesen Repo

#### 2- Setze deine .env Variablen mit der .env.template

```
# Falls Sie OpenAI als Provider verwenden möchten, fügen Sie nur das Modell und api_key hinzu.
LLM_API_KEY=""
LLM_MODEL="openai/gpt-4o-mini"
# Nicht benötigt, wenn Sie OpenAI
LLM_PROVIDER="openai"
LLM_ENDPOINT=""
LLM_API_VERSION=""

# Falls Sie OpenAI als Provider verwenden möchten, fügen Sie nur das Modell und api_key hinzu.
EMBEDDING_API_KEY=""
EMBEDDING_MODEL="openai/text-embedding-3-large"
# Nicht benötigt, wenn Sie OpenAI
EMBEDDING_PROVIDER="openai"
EMBEDDING_ENDPOINT=""
EMBEDDING_API_VERSION=""

# Notwendig für dieses Projekt
GITHUB_TOKEN=""

MIGRATION_DB_PROVIDER=sqlite
MIGRATION_DB_NAME=github. b      
MIGRATION_DB_PATH=/path_to_your_datasette_cognee/datasette-cognee # ersetzen Sie mit dem Pfad zu Ihrem geklonten datasette-cognee

```

#### 3- Führe folgendes aus

1. python -m venv venv && source venv/bin/activate && pip install -e .
2. datasette cognee relational-migrate github.db
3. datasette cognee Abfrage "Welche Informationen sind in der Datenbank?"
4. datasette serve github.db # (siehe was in der db)

\--

- Visualisieren Sie das Diagramm in Ihrem Home-Verzeichnis.
- Du kannst github löschen. b in diesem Repo und verwenden Sie das github-to-sqlite Plugin von datasette, um frisch mit dem Repository Ihrer Wahl zu beginnen, oder Sie können ein neues Repo zu cognee hinzufügen, indem Sie einfach `github-to-sqlite contributors github. b Besitzer/Repo`.


