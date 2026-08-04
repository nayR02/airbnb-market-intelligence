-- database/schema.sql
-- Airbnb Market Intelligence Database Schema
-- Follows 3NF normalization: no redundant data across tables.

PRAGMA foreign_keys = ON;

-- ── Hosts ─────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS hosts (
    host_id          INTEGER PRIMARY KEY,
    host_name        TEXT    NOT NULL DEFAULT 'Unknown',
    is_superhost     BOOLEAN
);

-- ── Neighbourhoods ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS neighbourhoods (
    neighbourhood_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name             TEXT    NOT NULL,
    city             TEXT    NOT NULL,
    UNIQUE(name, city)
);

-- ── Listings ──────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS listings (
    listing_id       INTEGER PRIMARY KEY,
    name             TEXT,
    host_id          INTEGER NOT NULL,
    neighbourhood_id INTEGER NOT NULL,
    latitude         REAL,
    longitude        REAL,
    room_type        TEXT,
    price            REAL    NOT NULL,
    minimum_nights   INTEGER,
    availability_365 INTEGER,
    city             TEXT    NOT NULL,

    FOREIGN KEY (host_id)          REFERENCES hosts(host_id),
    FOREIGN KEY (neighbourhood_id) REFERENCES neighbourhoods(neighbourhood_id)
);

-- ── Reviews ───────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS reviews (
    review_id            INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id           INTEGER NOT NULL UNIQUE,
    number_of_reviews    INTEGER DEFAULT 0,
    review_scores_rating REAL,

    FOREIGN KEY (listing_id) REFERENCES listings(listing_id)
);