# scraper/config.py
"""
Project-wide configuration settings.
All paths, constants, and city mappings live here.
Never hardcode these values in other files.
"""

from pathlib import Path

# ── Root of the project ───────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ── Data directories ──────────────────────────────────────────────
RAW_DIR    = BASE_DIR / "data" / "raw"
CLEANED_DIR = BASE_DIR / "data" / "cleaned"
ARCHIVE_DIR = BASE_DIR / "data" / "archive"

# ── Cities we're analysing ────────────────────────────────────────
CITIES = {
    "bangkok": "bangkok-listings.csv.gz",
    "sydney":  "sydney-listings.csv.gz",
    "london":  "london-listings.csv.gz",
}

# ── Columns we actually need from the raw file ────────────────────
REQUIRED_COLUMNS = [
    "id",
    "name",
    "host_id",
    "host_name",
    "host_is_superhost",
    "neighbourhood_cleansed",
    "latitude",
    "longitude",
    "room_type",
    "price",
    "minimum_nights",
    "number_of_reviews",
    "review_scores_rating",
    "availability_365",
]