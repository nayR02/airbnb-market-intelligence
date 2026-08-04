"""
Cleans raw Airbnb listing data.
Handles price formatting, nulls, and data types.
"""

import pandas as pd
from loguru import logger
from scraper.config import CLEANED_DIR


def clean_price(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert price from string '$1,234.00' to float 1234.00.
    Drops rows where price is null or zero.

    Args:
        df: Raw DataFrame with string price column.

    Returns:
        DataFrame with numeric price column.
    """
    before = len(df)

    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace(r"[\$,]", "", regex=True)
        .str.strip()
    )

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df[df["price"].notna() & (df["price"] > 0)].copy()
    
    after = len(df)
    logger.info(f"Price cleaning: dropped {before - after:,} rows")
    return df


def clean_superhost(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert host_is_superhost from 't'/'f' string to boolean.

    Args:
        df: DataFrame with string superhost column.

    Returns:
        DataFrame with boolean superhost column.
    """
    df["host_is_superhost"] = df["host_is_superhost"].map({"t": True, "f": False})
    return df


def clean_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle remaining null values.
    - Drops rows with null minimum_nights.
    - Fills null host_name with 'Unknown'.
    - Leaves review_scores_rating nulls (valid — listing has no reviews yet).

    Args:
        df: DataFrame after price and superhost cleaning.

    Returns:
        DataFrame with nulls handled.
    """
    df = df.dropna(subset=["minimum_nights"]).copy()
    df["host_name"] = df["host_name"].fillna("Unknown")
    return df


def clean_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enforce correct data types on all columns.

    Args:
        df: DataFrame after null handling.

    Returns:
        DataFrame with correct dtypes.
    """
    df["minimum_nights"] = df["minimum_nights"].astype(int)
    df["host_id"] = df["host_id"].astype(int)
    return df


def run_cleaning_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Run all cleaning steps in order.

    Args:
        df: Raw combined DataFrame from loader.

    Returns:
        Cleaned DataFrame ready for analysis.
    """
    logger.info("Starting cleaning pipeline...")

    df = clean_price(df)
    df = clean_superhost(df)
    df = clean_nulls(df)
    df = clean_dtypes(df)

    logger.success(f"Cleaning complete. Final shape: {df.shape}")
    return df


def save_cleaned(df: pd.DataFrame) -> None:
    """
    Save cleaned DataFrame to the cleaned data directory.

    Args:
        df: Cleaned DataFrame to save.
    """
    CLEANED_DIR.mkdir(parents=True, exist_ok=True)
    output_path = CLEANED_DIR / "listings_cleaned.csv"
    df.to_csv(output_path, index=False)
    logger.success(f"Saved cleaned data to {output_path}")