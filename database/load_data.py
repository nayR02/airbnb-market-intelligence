# database/load_data.py
"""
Loads cleaned Airbnb data into SQLite database.
Uses SQLAlchemy for database connection management.
"""

import sqlite3
import pandas as pd
from loguru import logger
from pathlib import Path
from scraper.config import CLEANED_DIR, BASE_DIR


DB_PATH     = BASE_DIR / "database" / "airbnb.db"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"
CLEANED_CSV = CLEANED_DIR / "listings_cleaned.csv"


def get_connection() -> sqlite3.Connection:
    """Create and return a SQLite database connection."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_schema(conn: sqlite3.Connection) -> None:
    """Run the SQL schema file to create all tables."""
    sql = SCHEMA_PATH.read_text()
    conn.executescript(sql)
    conn.commit()
    logger.info("Schema created successfully")


def load_hosts(df: pd.DataFrame, conn: sqlite3.Connection) -> None:
    """
    Extract unique hosts from listings and insert into hosts table.

    Args:
        df: Cleaned listings DataFrame.
        conn: SQLite connection.
    """
    hosts = (
        df[["host_id", "host_name", "host_is_superhost"]]
        .drop_duplicates(subset="host_id")
        .rename(columns={"host_is_superhost": "is_superhost"})
    )
    hosts.to_sql("hosts", conn, if_exists="append", index=False)
    logger.success(f"Inserted {len(hosts):,} hosts")


def load_neighbourhoods(df: pd.DataFrame, conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Extract unique neighbourhoods and insert into neighbourhoods table.
    Returns DataFrame with neighbourhood_id for use in listings.

    Args:
        df: Cleaned listings DataFrame.
        conn: SQLite connection.

    Returns:
        DataFrame mapping neighbourhood name+city to neighbourhood_id.
    """
    neighbourhoods = (
        df[["neighbourhood_cleansed", "city"]]
        .drop_duplicates()
        .rename(columns={"neighbourhood_cleansed": "name"})
        .reset_index(drop=True)
    )
    neighbourhoods.to_sql("neighbourhoods", conn, if_exists="append", index=False)

    # Read back with generated IDs
    neighbourhood_map = pd.read_sql(
        "SELECT neighbourhood_id, name, city FROM neighbourhoods", conn
    )
    logger.success(f"Inserted {len(neighbourhoods):,} neighbourhoods")
    return neighbourhood_map


def load_listings(
    df: pd.DataFrame,
    neighbourhood_map: pd.DataFrame,
    conn: sqlite3.Connection
) -> None:
    """
    Insert listings into the listings table with neighbourhood_id foreign key.

    Args:
        df: Cleaned listings DataFrame.
        neighbourhood_map: DataFrame mapping neighbourhood name+city to ID.
        conn: SQLite connection.
    """
    listings = df.merge(
    neighbourhood_map,
    left_on=["neighbourhood_cleansed", "city"],
    right_on=["name", "city"],
    how="left",
    suffixes=("", "_neighbourhood")
)

    listings = listings[[
    "id", "name", "host_id", "neighbourhood_id",
        "latitude", "longitude", "room_type",
        "price", "minimum_nights", "availability_365", "city"
    ]].rename(columns={"id": "listing_id"})

    listings.to_sql("listings", conn, if_exists="append", index=False)
    logger.success(f"Inserted {len(listings):,} listings")


def load_reviews(df: pd.DataFrame, conn: sqlite3.Connection) -> None:
    """
    Insert review summaries into the reviews table.

    Args:
        df: Cleaned listings DataFrame.
        conn: SQLite connection.
    """
    reviews = df[["id", "number_of_reviews", "review_scores_rating"]].rename(
        columns={"id": "listing_id"}
    )
    reviews.to_sql("reviews", conn, if_exists="append", index=False)
    logger.success(f"Inserted {len(reviews):,} review records")


def run_pipeline() -> None:
    """Run the full database loading pipeline."""
    logger.info("Starting database pipeline...")

    df = pd.read_csv(CLEANED_CSV, low_memory=False)
    conn = get_connection()

    create_schema(conn)
    load_hosts(df, conn)
    neighbourhood_map = load_neighbourhoods(df, conn)
    load_listings(df, neighbourhood_map, conn)
    load_reviews(df, conn)

    conn.close()
    logger.success(f"Database ready at {DB_PATH}")


if __name__ == "__main__":
    run_pipeline()