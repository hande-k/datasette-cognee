import asyncio
import logging
import click
import os

import cognee
from cognee.api.v1.search import SearchType
from cognee.shared.logging_utils import get_logger
from cognee.api.v1.visualize.visualize import visualize_graph

from cognee import prune
from cognee.low_level import setup
from cognee.infrastructure.databases.relational import get_migration_relational_engine
from cognee.infrastructure.databases.graph import get_graph_engine
from cognee.tasks.ingestion.migrate_relational_database import migrate_relational_database

from datasette import hookimpl

logger = get_logger()
logger.setLevel(logging.ERROR)


@hookimpl
def register_commands(cli):
    """
    Defines new datasette CLI commands for cognee:
    
    1) datasette cognee relational-migrate <DB_PATH> [--reset/--no-reset] # default is to reset (prune)
    2) datasette cognee query <QUERY_TEXT>
    """
    @cli.group(name="cognee")
    def cognee_group():
        """Commands for working with cognee."""
        pass

    @cognee_group.command(name="relational-migrate")
    @click.argument("db_path", type=click.Path(exists=True))
    @click.option("--reset/--no-reset", default=True, help="Prune Cognee data before migration?")
    def cognee_relational_migrate(db_path, reset):
        """
        Migrate the SQLite database into knowledge graph 
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(_async_cognee_relational_migrate(db_path, reset))
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

    @cognee_group.command(name="query")
    @click.argument("query_text", type=str)
    def cognee_query(query_text):
        """
        Query the knowledge graph.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(_async_cognee_query(query_text))
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

    return [cognee_group]


async def _async_cognee_relational_migrate(db_path, reset):
    """
    Async function to, prune, setup, extract schema, migrate, and visualize.
    """
    if reset:
        print("Pruning data...")
        await prune.prune_data()
        await prune.prune_system(metadata=True)
        print("Prune complete.\n")

    await setup()
    print(f"Extracting schema from {db_path} ...")
    relational_engine = get_migration_relational_engine()
    schema = await relational_engine.extract_schema()
    print(f"Found tables: {list(schema.keys())}\n")

    print("Building graph engine...")
    graph_engine = await get_graph_engine()

    print("Starting relational migration...")
    await migrate_relational_database(graph_engine, schema=schema)
    print("Migration complete!\n")

    print("Rendering graph visualization...")
    await visualize_graph()

async def _async_cognee_query(query_text):
    """
    Async function to query the knowledge graph.
    """
    print(f"Querying with: '{query_text}'")

    search_results = await cognee.search(
        query_type=SearchType.GRAPH_COMPLETION,
        query_text=query_text
    )

    print(f"Search results: {search_results}")