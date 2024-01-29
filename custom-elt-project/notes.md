### Creating the Docker Image

`docker-compose up -d`

`docker ps`
```bash
24b914aee03f   postgres:latest   "docker-entrypoint.s…"   12 minutes ago   Up 12 minutes   0.0.0.0:5434->5432/tcp, :::5434->5432/tcp   custom-elt-project_destination_postgres_1
e8530538169c   postgres:latest   "docker-entrypoint.s…"   12 minutes ago   Up 12 minutes   0.0.0.0:5433->5432/tcp, :::5433->5432/tcp   custom-elt-project_source_postgres_1
```

`docker exec -it custom-elt-project_destination_postgres_1 psql -U postgres`

### Connect to the DB

```bash
\c destination_db
\dt

             List of relations
 Schema |     Name      | Type  |  Owner   
--------+---------------+-------+----------
 public | actors        | table | postgres
 public | film_actors   | table | postgres
 public | film_category | table | postgres
 public | films         | table | postgres
 public | users         | table | postgres
```

```bash
SELECT * FROM users;
SELECT DISTINCT email FROM users;
UPDATE users SET email = 'new_email@gmail.com' WHERE first_name='John';
SELECT * FROM films LIMIT 5;
SELECT COUNT(*) from films;
SELECT SUM(price) from films;
SELECT MAX(price), MIN(price) from films;
SELECT AVG(user_rating) from films;
SELECT rating, AVG(user_rating) from films GROUP BY rating;

SELECT
    f.film_id,
    f.title,
    a.actor_name
FROM
    films f
INNER JOIN
    film_actors fa ON f.film_id = fa.film_id
INNER JOIN
    actors a ON fa.actor_id = a.actor_id
ORDER BY
    f.film_id;


SELECT
    f.film_id,
    f.title,
    a.actor_name
FROM
    films f
LEFT JOIN
    film_actors fa ON f.film_id = fa.film_id
LEFT JOIN
    actors a ON fa.actor_id = a.actor_id
ORDER BY
    f.film_id;

SELECT
    title as name
FROM
    films
UNION
SELECT
    actor_name as name
FROM
    actors
ORDER BY
    name;


SELECT
    title as name
FROM
    films
UNION
SELECT
    actor_name as actor
FROM
    actors
ORDER BY
    name;

--Subqueries
SELECT
    title,
(SELECT actor_name
FROM actors a
JOIN film_actors fa ON a.actor_id = fa.actor_id
WHERE fa.film_id = f.film_id
LIMIT 1) AS actor_name
FROM films f;


SELECT
    title
FROM films
WHERE film_id IN
(SELECT fa.film_id
FROM film_actors fa
JOIN actors a ON a.actor_id = fa.actor_id
WHERE a.actor_name IN ('Leonardo DiCaprio', 'Tom Hanks'));
```