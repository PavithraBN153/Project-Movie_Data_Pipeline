-- ---------------------------------------------
-- Movie Database Schema
-- 2 Tables: movies, ratings
-- Designed to work with ETL.py
-- ---------------------------------------------

-- DROP TABLES IF THEY EXIST (safe to run multiple times)
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS movies;

-- -------------------------------
-- Movies Table
-- Stores movie information
-- -------------------------------
CREATE TABLE movies (
    movie_id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    genres VARCHAR(255),
    release_year INT,
    director VARCHAR(255)
);

-- -------------------------------
-- Ratings Table
-- Stores user ratings
-- -------------------------------
CREATE TABLE ratings (
    rating_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    rating FLOAT,
    rating_timestamp DATETIME,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);

