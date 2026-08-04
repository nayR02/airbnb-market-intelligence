"""
Exploratory Data Analysis for Airbnb Market Intelligence.
Answers key business questions using SQL + pandas.
"""

import sqlite3
import pandas as pd
from loguru import logger
from scraper.config import BASE_DIR

DB_PATH = BASE_DIR / "database" / "airbnb.db"


def get_connection() -> sqlite3.Connection:
    """Return a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)


def most_expensive_cities(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Q1: What is the average nightly price per city?
    Business use: helps investors compare markets at a glance.
    """
    query = """
        SELECT
            city,
            ROUND(AVG(price), 2)  AS avg_price,
            ROUND(MIN(price), 2)  AS min_price,
            ROUND(MAX(price), 2)  AS max_price,
            COUNT(*)              AS total_listings
        FROM listings
        GROUP BY city
        ORDER BY avg_price DESC
    """
    return pd.read_sql(query, conn)


def price_by_room_type(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Q2: How does price vary by room type across cities?
    Business use: understand what type of property commands premium pricing.
    """
    query = """
        SELECT
            city,
            room_type,
            ROUND(AVG(price), 2) AS avg_price,
            COUNT(*)             AS total_listings
        FROM listings
        GROUP BY city, room_type
        ORDER BY city, avg_price DESC
    """
    return pd.read_sql(query, conn)


def superhost_impact(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Q3: Do superhosts charge more or get better ratings?
    Business use: quantify the superhost badge value.
    """
    query = """
        SELECT
            l.city,
            h.is_superhost,
            ROUND(AVG(l.price), 2)        AS avg_price,
            ROUND(AVG(r.review_scores_rating), 2) AS avg_rating,
            COUNT(*)                       AS total_listings
        FROM listings l
        JOIN hosts h ON l.host_id = h.host_id
        JOIN reviews r ON l.listing_id = r.listing_id
        WHERE h.is_superhost IS NOT NULL
        GROUP BY l.city, h.is_superhost
        ORDER BY l.city, h.is_superhost DESC
    """
    return pd.read_sql(query, conn)


def top_neighbourhoods(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Q4: Which neighbourhoods have the most listings per city?
    Business use: identify supply hotspots for market saturation analysis.
    """
    query = """
        SELECT
            l.city,
            n.name              AS neighbourhood,
            COUNT(*)            AS total_listings,
            ROUND(AVG(l.price), 2) AS avg_price
        FROM listings l
        JOIN neighbourhoods n ON l.neighbourhood_id = n.neighbourhood_id
        GROUP BY l.city, n.name
        ORDER BY l.city, total_listings DESC
    """
    return pd.read_sql(query, conn)


def rating_distribution(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Q5: What does the rating distribution look like per city?
    Business use: measure overall guest satisfaction by market.
    """
    query = """
        SELECT
            l.city,
            ROUND(AVG(r.review_scores_rating), 2) AS avg_rating,
            COUNT(CASE WHEN r.review_scores_rating >= 4.8 THEN 1 END) AS excellent,
            COUNT(CASE WHEN r.review_scores_rating BETWEEN 4.0 AND 4.79 THEN 1 END) AS good,
            COUNT(CASE WHEN r.review_scores_rating < 4.0 THEN 1 END) AS poor,
            COUNT(CASE WHEN r.review_scores_rating IS NULL THEN 1 END) AS no_rating
        FROM listings l
        JOIN reviews r ON l.listing_id = r.listing_id
        GROUP BY l.city
    """
    return pd.read_sql(query, conn)


if __name__ == "__main__":
    conn = get_connection()

    logger.info("Q1: Most expensive cities")
    print(most_expensive_cities(conn).to_string(index=False))

    logger.info("Q2: Price by room type")
    print(price_by_room_type(conn).to_string(index=False))

    logger.info("Q3: Superhost impact")
    print(superhost_impact(conn).to_string(index=False))

    logger.info("Q4: Top neighbourhoods")
    print(top_neighbourhoods(conn).to_string(index=False))

    logger.info("Q5: Rating distribution")
    print(rating_distribution(conn).to_string(index=False))

    conn.close()