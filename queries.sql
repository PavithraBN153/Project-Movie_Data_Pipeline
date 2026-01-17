-- ---------------------------------------------
-- Query 1: Movie with the highest average rating
-- ---------------------------------------------
SELECT 
    m.title,
    AVG(r.rating) AS avg_rating
FROM movies m
JOIN ratings r 
    ON m.movie_id = r.movie_id
GROUP BY m.movie_id, m.title
ORDER BY avg_rating DESC
LIMIT 1;


-- ---------------------------------------------
-- Query 2: Top 5 movie genres with highest average rating
-- (Using first genre for simplicity)
-- ---------------------------------------------
SELECT 
    SUBSTRING_INDEX(m.genres, '|', 1) AS genre,
    AVG(r.rating) AS avg_rating
FROM movies m
JOIN ratings r 
    ON m.movie_id = r.movie_id
GROUP BY genre
ORDER BY avg_rating DESC
LIMIT 5;


-- ---------------------------------------------
-- Query 3: Director with the most movies
-- ---------------------------------------------
SELECT 
    director,
    COUNT(*) AS movie_count
FROM movies
WHERE director IS NOT NULL
  AND director <> 'N/A'
GROUP BY director
ORDER BY movie_count DESC
LIMIT 1;


-- ---------------------------------------------
-- Query 4: Average rating of movies by release year
-- ---------------------------------------------
SELECT 
    m.release_year,
    AVG(r.rating) AS avg_rating
FROM movies m
JOIN ratings r 
    ON m.movie_id = r.movie_id
WHERE m.release_year IS NOT NULL
GROUP BY m.release_year
ORDER BY m.release_year;
