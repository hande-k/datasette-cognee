# datasette-cognee

## Introduction
This is a plugin for Datasette that integrates with cognee to provide knowledge graph capabilities for Datasette databases. 

cognee allows you to ingest structured data from SQLite databases into a knowledge graph and perform semantic queries against that graph.

## Project to discover repository contributors

This project utilizes https://github.com/dogsheep/github-to-sqlite for fetching GitHub data to SQLite database to be migrated into cognee. 

As the default database, https://github.com/dogsheep/github-to-sqlite?tab=readme-ov-file#fetching-contributors-to-a-repository is used to fetch contributors of cognee. 

```
github-to-sqlite contributors github.db topoteretes/cognee
```

Do the following for a quick test:

#### 1- Clone this repo

#### 2- Set your .env variables using the .env.template

```
# In case you choose to use OpenAI as a provider, add just the model and api_key.
LLM_API_KEY=""
LLM_MODEL="openai/gpt-4o-mini"
# Not needed if you use OpenAI
LLM_PROVIDER="openai"
LLM_ENDPOINT=""
LLM_API_VERSION=""

# In case you choose to use OpenAI as a provider, add just the model and api_key.
EMBEDDING_API_KEY=""
EMBEDDING_MODEL="openai/text-embedding-3-large"
# Not needed if you use OpenAI
EMBEDDING_PROVIDER="openai"
EMBEDDING_ENDPOINT=""
EMBEDDING_API_VERSION=""

# Necessary for this project
GITHUB_TOKEN=""

MIGRATION_DB_PROVIDER=sqlite
MIGRATION_DB_NAME=github.db      
MIGRATION_DB_PATH=/path_to_your_datasette_cognee/datasette-cognee # replace with the path to your cloned datasette-cognee

```

#### 3- Run the following

1. python -m venv venv && source venv/bin/activate && pip install -e .
2. datasette cognee relational-migrate github.db    
3. datasette cognee query "What information is in the database?"
4. datasette serve github.db # (see whats in the db)

--
- Visualize the graph in your home directory.
- You can delete github.db in this repo and use the github-to-sqlite plugin from datasette to start fresh with the repository of your choice or you can add a new repo to cognee by simply running `github-to-sqlite contributors github.db owner/repo`. 


