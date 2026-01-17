import pandas as pd
import mysql.connector
import requests
import time  # optional: to avoid hitting OMDb API too fast

# -------------------------------
# CONFIGURATION
# -------------------------------

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "movie_db"
}

OMDB_API_KEY = "81e3c9ae"

MOVIES_CSV = "movies.csv"
RATINGS_CSV = "ratings.csv"


# -------------------------------
# OMDb EXTRACTION FUNCTION
# -------------------------------

def extract_from_omdb(movie_name):
    """
    Calls OMDb API to get director and year for a given movie.
    Handles missing movies gracefully.
    """
    clean_name = movie_name.split('(')[0].strip()  # remove year in parentheses
    url = "http://www.omdbapi.com/"
    params = {
        "t": clean_name,
        "apikey": OMDB_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if data.get("Response") == "True":
            movie_director = data.get("Director")
            movie_year = data.get("Year")
            return movie_director, movie_year
        else:
            print(f"OMDb movie not found: {movie_name}")
            return None, None

    except Exception as e:
        print(f"OMDb error for {movie_name}: {e}")
        return None, None


# -------------------------------
# MAIN ETL PROCESS
# -------------------------------

print("ETL started")

# 1️. Connect to MySQL
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()
print("Connected to database")

# 2️. Read CSV files
movies_df = pd.read_csv(MOVIES_CSV).head(2000)
movie_ids = set(movies_df["movieId"])
ratings_df = pd.read_csv(RATINGS_CSV)
ratings_df = ratings_df[ratings_df["movieId"].isin(movie_ids)]

# -------------------------------
# Load Movies
# -------------------------------

for _, row in movies_df.iterrows():
    movie_id = int(row["movieId"])
    movie_title = row["title"]
    genres = row["genres"]

    # Extract year from title if present e.g. "Movie Name (1999)"
    release_year = None
    if "(" in movie_title and ")" in movie_title:
        try:
            release_year = int(movie_title[-5:-1])
            movie_title = movie_title[:-7].strip()
        except:
            pass

    # Extract from OMDb
    movie_director, omdb_year = extract_from_omdb(movie_title)

    # Prefer OMDb year if available
    if omdb_year and omdb_year.isdigit():
        release_year = int(omdb_year)

    # Insert into database (idempotent)
    cursor.execute(
        """
        INSERT INTO movies (movie_id, title, genres, release_year, director)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            title = VALUES(title),
            genres = VALUES(genres),
            release_year = VALUES(release_year),
            director = VALUES(director)
        """,
        (movie_id, movie_title, genres, release_year, movie_director)
    )

    # Optional: delay to avoid API rate limits
    time.sleep(0.1)

conn.commit()
print("Movies loaded")

# -------------------------------
# Load Ratings
# -------------------------------

for _, row in ratings_df.iterrows():
    cursor.execute(
        """
        INSERT INTO ratings (user_id, movie_id, rating, rating_timestamp)
        VALUES (%s, %s, %s, FROM_UNIXTIME(%s))
        """,
        (
            int(row["userId"]),
            int(row["movieId"]),
            float(row["rating"]),
            int(row["timestamp"])
        )
    )

conn.commit()
print("Ratings loaded")

# -------------------------------
# Close Connection
# -------------------------------

cursor.close()
conn.close()
print("ETL completed successfully")
