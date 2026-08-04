# scraper/loader.py
"""
Loads raw Airbnb listing files into pandas DataFrames.
Handles .csv.gz files directly without manual extraction.
"""

import pandas as pd
from loguru import logger
from scraper.config import RAW_DIR, CITIES, REQUIRED_COLUMNS


def load_city(city: str) -> pd.DataFrame:
    """
    Load a single city's raw listings file.

    Args:
        city: City key matching one in CITIES config (e.g. 'bangkok').

    Returns:
        DataFrame containing only the required columns.

    Raises:
        ValueError: If the city key is not found in config.
        FileNotFoundError: If the raw file doesn't exist.
    """
    if city not in CITIES:
        raise ValueError(f"Unknown city '{city}'. Available: {list(CITIES.keys())}")

    filepath = RAW_DIR / CITIES[city]

    if not filepath.exists():
        raise FileNotFoundError(f"Raw file not found: {filepath}")

    logger.info(f"Loading {city} from {filepath.name}...")

    df = pd.read_csv(filepath, usecols=REQUIRED_COLUMNS, low_memory=False)
    df["city"] = city  # tag each row with its city

    logger.success(f"Loaded {city}: {len(df):,} listings")
    return df


def load_all_cities() -> pd.DataFrame:
    """
    Load all cities defined in config and combine into one DataFrame.

    Returns:
        Combined DataFrame with a 'city' column identifying each row.
    """
    frames = []

    for city in CITIES:
        df = load_city(city)
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)
    logger.success(f"Total listings loaded: {len(combined):,}")
    return combined