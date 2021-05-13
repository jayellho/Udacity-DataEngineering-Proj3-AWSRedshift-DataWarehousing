import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')
ARN = config.get("IAM_ROLE", "ARN")
LOG_DATA = config.get("S3","LOG_DATA")
LOG_JSONPATH = config.get("S3","LOG_JSONPATH")
SONG_DATA = config.get("S3","SONG_DATA")

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
    CREATE TABLE staging_events (
        artist VARCHAR,
        auth VARCHAR,
        first_name VARCHAR,
        gender VARCHAR(1),
        item_in_session INTEGER,
        last_name VARCHAR,
        length DECIMAL,
        level VARCHAR,
        location VARCHAR,
        method VARCHAR,
        page VARCHAR,
        registration VARCHAR(50),
        session_id INTEGER,
        song VARCHAR,
        status INTEGER,
        ts BIGINT,
        user_agent VARCHAR,
        user_id INTEGER
        
    )
""")

staging_songs_table_create = ("""
    CREATE TABLE staging_songs (
        num_songs INTEGER,
        artist_id VARCHAR,
        artist_latitude NUMERIC,
        artist_longitude NUMERIC,
        artist_location VARCHAR,
        artist_name VARCHAR,
        song_id VARCHAR,
        title VARCHAR,
        duration DECIMAL,
        year INTEGER
    )
""")

songplay_table_create = ("""
    CREATE TABLE songplays (
        songplay_id INTEGER IDENTITY(0,1) NOT NULL PRIMARY KEY,
        start_time TIMESTAMP NOT NULL,
        user_id INTEGER NOT NULL,
        level VARCHAR,
        song_id VARCHAR NOT NULL,
        artist_id VARCHAR NOT NULL,
        session_id INTEGER NOT NULL,
        location VARCHAR,
        user_agent VARCHAR
    )
""")

user_table_create = ("""
    CREATE TABLE users (
        user_id INTEGER NOT NULL PRIMARY KEY,
        first_name VARCHAR,
        last_name VARCHAR,
        gender VARCHAR(1),
        level VARCHAR        
    )
""")

song_table_create = ("""
    CREATE TABLE songs (
        song_id VARCHAR NOT NULL PRIMARY KEY,
        title VARCHAR,
        artist_id VARCHAR NOT NULL,
        year INTEGER,
        duration DECIMAL
    )
""")

artist_table_create = ("""
    CREATE TABLE artists (
        artist_id VARCHAR NOT NULL PRIMARY KEY,
        name VARCHAR,
        location VARCHAR,
        latitude NUMERIC,
        longitude NUMERIC
    )
""")

time_table_create = ("""
    CREATE TABLE time (
        start_time TIMESTAMP NOT NULL PRIMARY KEY,
        hour INTEGER NOT NULL,
        day INTEGER NOT NULL,
        week INTEGER NOT NULL,
        month INTEGER NOT NULL,
        year INTEGER NOT NULL,
        weekday INTEGER NOT NULL
    )
""")

# STAGING TABLES

staging_events_copy = ("""
    COPY staging_events FROM {}
    IAM_ROLE '{}'
    JSON {};
""").format(LOG_DATA, ARN, LOG_JSONPATH)

staging_songs_copy = ("""
    COPY staging_songs FROM {}
    IAM_ROLE '{}'
    JSON 'auto';
""").format(SONG_DATA, ARN)

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays 
        (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT TIMESTAMP 'epoch' + se.ts/1000 * interval '1 second' as start_time,
        se.user_id AS user_id,
        se.level AS level,
        ss.song_id AS song_id,
        ss.artist_id AS artist_id,
        se.session_id AS session_id,
        se.location AS location,
        se.user_agent AS user_agent
    FROM staging_events AS se
    JOIN staging_songs AS ss ON se.artist = ss.artist_name
    WHERE se.page = 'NextSong'
""")

user_table_insert = ("""
    INSERT INTO users
        (user_id, first_name, last_name, gender, level)
    SELECT
        DISTINCT user_id,
        first_name,
        last_name,
        gender,
        level
    FROM staging_events
    WHERE page = 'NextSong' AND user_id IS NOT NULL
""")

song_table_insert = ("""
    INSERT INTO songs
        (song_id, title, artist_id, year, duration)
    SELECT
        DISTINCT song_id,
        title,
        artist_id,
        year,
        duration
    FROM staging_songs
    WHERE song_id IS NOT NULL
""")

artist_table_insert = ("""
    INSERT INTO artists
        (artist_id, name, location, latitude, longitude)
    SELECT
        DISTINCT artist_id,
        artist_name,
        artist_location,
        artist_latitude,
        artist_longitude
    FROM staging_songs
    WHERE artist_id IS NOT NULL
""")

time_table_insert = ("""
    INSERT INTO time
        (start_time, hour, day, week, month, year, weekday)
    SELECT
        DISTINCT TIMESTAMP 'epoch' + se.ts/1000 * INTERVAL '1 second' AS start_time,
        EXTRACT (hour FROM start_time) AS hour,
        EXTRACT (day FROM start_time) AS day,
        EXTRACT (week FROM start_time) AS week,
        EXTRACT (month FROM start_time) AS month,
        EXTRACT (year FROM start_time) AS year,
        EXTRACT (weekday FROM start_time) AS weekday
    FROM staging_events AS se
    WHERE se.page = 'NextSong';
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
