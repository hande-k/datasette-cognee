import asyncio
import logging
import click

# Cognee imports
import cognee
from cognee.api.v1.search import SearchType
from cognee.shared.utils import setup_logging

from datasette import hookimpl

@hookimpl
def register_commands(cli):
    """
    Defines new datasette CLI commands:
    - datasette -- cognee ingest <DB_PATH> <TABLE_NAME> ...
    - datasette -- cognee query  <QUERY_TEXT> ...
    """
    @cli.group(name="cognee")
    def cognee_group():
        """Commands for working with Cognee."""
        pass

    @cognee_group.command(name="ingest")
    @click.argument("db_path", type=click.Path(exists=True))
    @click.argument("table_name", type=str)
    @click.option("--reset/--no-reset", default=True, help="Whether to prune cognee data before ingesting new data.")
    def cognee_ingest(db_path, table_name, reset):
        # We'll run an async function to ingest data.
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(_async_cognee_ingest(db_path, table_name, reset))
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

    @cognee_group.command(name="query")
    @click.argument("query_text", type=str)
    def cognee_query(query_text):
        # We'll run an async function to query data.
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(_async_cognee_query(query_text))
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

    return [cognee_group]

async def _async_cognee_ingest(db_path, table_name, reset):
    """
    Async function to reset Cognee data (optional),
    read from a SQLite table, add text to Cognee, and run cognify().
    """
    setup_logging(logging.ERROR)

    if reset:
        print("Pruning Cognee data...")
        await cognee.prune.prune_data()
        await cognee.prune.prune_system(metadata=True)
        print("Prune complete.\n")

    # Connect to SQLite, read from table
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    col_names = [desc[0] for desc in cursor.description]
    count = 0

    # Send each row's text to Cognee
    for row in rows:
        row_dict = dict(zip(col_names, row))
        # Convert row into a simple string representation
        text_content = str(row_dict)

        # Add to Cognee
        await cognee.add(text_content)
        count += 1

    print(f"Added {count} rows from {table_name} to Cognee.")

    # Now run cognify to build the knowledge graph
    print("\nRunning cognify() to generate knowledge graph ...")
    await cognee.cognify()
    print("Cognify done.")

async def _async_cognee_query(query_text):
    """
    Async function to query the knowledge graph using Cognee.
    """
    setup_logging(logging.ERROR)

    print(f"Querying Cognee with: '{query_text}'")
    search_results = await cognee.search(
        query_type=SearchType.INSIGHTS,
        query_text=query_text
    )

    # Display results
    print("Search results:")
    for idx, item in enumerate(search_results, start=1):
        print(f"{idx}. {item}")
    print()
