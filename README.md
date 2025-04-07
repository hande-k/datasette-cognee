# datasette-cognee

This is a plugin for Datasette that integrates with cognee to provide knowledge graph capabilities for Datasette databases. 

It allows you to ingest structured data from SQLite databases into a knowledge graph and perform semantic queries against that graph.

1. python -m venv venv && source venv/bin/activate && pip install -e .
2. datasette cognee relational-migrate github.db    
3. datasette cognee query "What information is in the database?"
4. datasette serve test.db # (see whats in the db)