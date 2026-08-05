"""
Exports SQLite tables to CSV files for Power BI consumption.
"""

import sqlite3
import pandas as pd
from loguru import logger
from scraper.config import BASE_DIR

DB_PATH     = BASE_DIR / "database" / "airbnb.db"
EXPORT_DIR  = BASE_DIR / "data" / "cleaned"


def export_table(conn: sqlite3.Connection, table: str) -> None:
    """
    Export a single SQLite table to CSV.

    Args:
        conn: SQLite connection.
        table: Table name to export.
    """
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    path = EXPORT_DIR / f"{table}.csv"
    df.to_csv(path, index=False)
    logger.success(f"Exported {table}: {len(df):,} rows → {path.name}")


def run_export() -> None:
    """Export all tables to CSV for Power BI."""
    conn = sqlite3.connect(DB_PATH)

    for table in ["listings", "hosts", "neighbourhoods", "reviews"]:
        export_table(conn, table)

    conn.close()
    logger.success("All tables exported.")


if __name__ == "__main__":
    run_export()