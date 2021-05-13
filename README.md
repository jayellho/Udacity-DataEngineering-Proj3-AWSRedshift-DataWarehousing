# Project: Building a Data Warehouse for Sparkify (a music streaming startup)

## Introduction
A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.
  
As their data engineer, you are tasked with building an <b>ETL pipeline</b> that <b>extracts</b> their data from <b>S3</b>, <b>stages</b> them in <b>Redshift</b>, and <b>transforms</b> data into a set of <b>dimensional tables</b> for their analytics team to continue finding insights in what songs their users are listening to. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.  


## Datasets
<u>Datasets residing in S3</u>
- Song data: `s3://udacity-dend/song-data`
- Log data: `s3://udacity-dend/log_data`
Log data json path: `s3://udacity-dend/log_json_path.json`

<u>Dataset 1: Song Data [Sample Format]</u>
``` json
{
    "num_songs" : 1,
    "artist_id" : "ARJIE2Y1187B994AB7",
    "artist_latitude" : null,
    "artist_longitude" : null, 
    "artist_location" : "",
    "artist_name" : "Line Renaud",
    "song_id" : "SOUPIRU12A6D4FA1E1",
    "title" : "Der Kleine Dompfaff",
    "duration" : 152.92036,
    "year": 0
}
```

<u>Dataset 2: Log Data [Sample Format] </u>
```json
{
    "artist" : "Pavement",
    "auth" : "Logged In",
    "firstName": "Sylvie",
    "gender": "F",
    "iteminSession": 0,
    "lastName": "Cruz",
    "length": 99.16036,
    "level": "free",
    "location": "Washington-Arlington-Alexandria, DC-VA-MD-WV",
    "method": "PUT",
    "page": "NextSong",
    "registration": "1.540266e+12",
    "sessionId": 345,
    "song": "Mercy: The Laundromat",
    "status": 200,
    "ts": 1541992058796,
    "userAgent": "\"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36\"",
    "userid": 24
}
```


## Database Schema
The chosen schema is a star schema optimised for queries on songplay analysis. The following are the included tables.

<u>Fact Table</u>
1. `songplays` - records in event data associated with song plays i.e. records with page <b>NextSong</b>
  * songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

<u>Dimensions Tables</u>
1. `users` - users in the app
  * user_id, first_name, last_name, gender, level

2. `songs` - songs in music database
  * song_id, title, artist_id, year, duration

3. `artists` - artists in music database
  * artist_id, name, location, latitude, longitude

4. `time` - timestamps of records in `songplays` broken down into specific units
  * start_time, hour, day, week, month, year, weekday


## Project Files
1. `create_table.py` - fact and dimension tables are created for the star schema in Redshift.

2. `etl.py` - S3 data are loaded into staging tables on Redshift before being processed into analytics tables on Redshift.

3. `sql_queries.py` - SQL statements are defined here and imported into the two above files.

4. `dwh.cfg` - contains details and authentication for Redshift including hostname, database user and password, ARN and paths to the respective datasets.

5. `README.md` - contains descriptions about the entire project and instructions on how this ETL pipeline works.

## Build
Pre-requisites:
  * Python 3
  * The following Python 3 libraries: `psycopg2`, `sql_queries`, `configparser`
  * Amazon Redshift cluster created.
  * IAM role with at least S3 read access.
 
## Instructions

1. Install Python 3 if you have not already.

2. Modify `dwh.cfg` first by launching a cluster on Redshift, creating an IAM role and user with at least S3 read access and getting the required credentials. Remember to save `dwh.cfg`.

2. In `sql_queries.py`, write the relevant SQL statements to delete tables if existing, create tables and insert rows into tables. This script does not need to be run as it is referred to in the other Python scripts below.

3. Create tables using `create_tables.py`. Run in terminal using the command `python create_tables.py` and ensure it runs smoothly. Check the table schemas in the Redshift database.

4. Perform the Extract, Transform, Load (ETL) operation by running `etl.py` using the command `python etl.py`. Test out queries as needed in the Redshift console's Query Editor.

5. If you have launched a Redshift cluster, remember to delete OR pause it (if you would like to reuse it) after this project. If not, you will be charged for letting it run.


