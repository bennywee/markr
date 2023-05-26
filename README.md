# markr
Data ingestion and processing microservice prototype.

# Run service locally
Execute the following command to build the docker image and run the application locally:

```
docker compose up markr
```

The application will expose `port 4567` on localhost. It will automatically create a SQLite3 database inside the docker container. You can run `cURL` commands to upload test scores (XML documents) as so:

```
curl -H "Content-Type: text/xml+markr"\
      -X POST localhost:4567/import/\
      -d @- <<XML
<mcq-test-results>
        <mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
            <first-name>Jane</first-name>
            <last-name>Austen</last-name>
            <student-number>521585128</student-number>
            <test-id>1234</test-id>
            <summary-marks available="20" obtained="13" />
        </mcq-test-result>
    </mcq-test-results>
XML
```

If all goes well you should receive a confirmation message: `Data uploaded successfully`. You can also send through an `.xml` file, like the `sample_results.xml` all at once:

```
curl -H "Content-Type: text/xml+markr"\
      -X POST http://127.0.0.1:4567/import/\
      -d @sample_results.xml
```

To query aggregate data for a given test id, we need to query the endpoint `/results/:test-id/aggregate`. 

```
curl http://localhost:4567/results/1234/aggregate
```

And this should return a json with the corresponding summary statistics for a given test id. 

# Run tests
Pytest is used to run unit tests. First build the development environment:

```
docker compose build dev
```

Then use docker compose to run the tests. You could also run the development container and just enter `python -m pytest` directly into the shell. 

```
docker compose run dev -c "python -m pytest"
```

## Test coverage
Executing `docker compose run dev -c "coverage run -m pytest & coverage report"` will produce the test coverage report:

```
Name                 Stmts   Miss  Cover
----------------------------------------
app/__init__.py          0      0   100%
app/data.py             14      0   100%
app/main.py             42      8    81%
tests/__init__.py        2      0   100%
tests/conftest.py       30      0   100%
tests/test_data.py      22      0   100%
tests/test_main.py      18      0   100%
----------------------------------------
TOTAL                  128      8    94%
```

# Solution design
This microservice is built using Flask in Python with SQLite3 as a persisted storage solution. Below is a high level descirption of the repo structure:

```
├── Dockerfile
├── README.md
├── app                  <-- All application code and SQL queries
│   ├── __init__.py
│   ├── data.py             <-- Functions to help parse XML data and produce summary statistics
│   ├── main.py             <-- Main application
│   ├── insert.sql          <-- Query writes parsed XML data into database
│   └── test_scores.sql     <-- Requests test data for summary statistic calculations
├── db                   <-- Database directory
│   ├── create_db.py        <-- Creates SQLite3 database
│   ├── ddl.sql             <-- Database schema (DDL: data definition language)
│   └── markr.db            <-- Database file - created when building and running app locally
├── docker-compose.yml
├── requirements.txt     <-- Python dependencies
└── tests                <-- Unit tests
    ├── __init__.py
    ├── conftest.py          <-- Unit test fixtures
    ├── test_data.py
    └── test_main.py
```
As noted, `markr.db` is the database which is created when running the application locally. The table `results` contains the test scores in the `markr` database. 

## Schema
The columns are defined and interpreted as:

- **created_datetime (string)**: Timestamp when record was first created in database
- **updated_datetime (string)**: Timestamp when record was last updated in database
- **scanned_datetime (string)**: Time when test was first scanned by machine
- **student_number (string)**: Student number (assumed to be unique for a given test)
- **test_id (string)**: Indexes the type of test taken 
- **obtained_marks (int)**: Number of marks received on given test
- **available_marks (int)**: Marks available on test
- **PRIMARY KEY (student_number, test_id)**

## Assumptions and design choices
**1) Uniqueness of the primary key**

I've assumed that each pair of student ids and test ids are unique and would therefore make a suitable primary key (PK). However, this would not be the case if say, the same test were conducted statewide or countrywide and the student id is unique within schools. It would be very easy for student ids to overlap between schools if this was the case and cause problems for our database.

If this is true, then it may be required to collect school id data and create a new PK with student, school and test ids. Using first or last name to form the PK would be insufficient as there may be an instance of two students with the same name and student id (and there are other reasons not to use name information as discussed next).

**2) Ignoring PII (personally identifiable information) data**

I deliberately avoided ingesting first and last name into columns of the table. In general, if the table was directly being used (or might be used) to populate production dashboards then PII data should not be so easily accessible at this layer.

At the very least, this information should be hashed in this table. But this data was not required as part of the service requirements. I discuss an alternative design pattern for this service in the next section which deals with this in a different way. 

**3) Dealing with duplicate documents**

Part of the product requirements is dealing with duplicate document scans (and to take the highest obtained and available scores). I chose to upsert (update and insert) the database table when this occurs. Line 9 onwards in `app/insert.sql` contains logic to handle an instance when a document is scanned twice (i.e when the primary key is duplicated). 

## Alternative solution design
An alternative approach to the database design would be to follow an ELT pattern. This approach would deal with points 2) and 3) in a different way. At a high level:

1) Ingest (extract and load) all the XML data into a SQL/NoSQL database (or in a data lake or some other storage).

2) Have separate logic remove the duplicate rows (and PII information) and write to a relational database - this would be where the aggregate endpoint would query

3) If name and last name columns are necessary, hash the values in the columns and restrict access to the raw data with PII information.

Pursuing this approach for this POC would involve creating two separate tables, one with the data dump and a second one which contains the clean data without any duplicates. However, this would've been more complicated given the time constraints. 

# Real time dashboards
To support a real live dashboard, it may be faster to query a table which contains the aggregated summary statistics. So instead of calling the API to perform the data transformation, have the dashboarding solution perform a SQL query to the aggregate table directly. This POC could be extended (or redesigned) to follow the ELT process above where one of the key outputs is a table with aggregated summary statistics. This assumes that it is faster to query a table than it is for the api to do the aggregate data transformation. Further thinking and assumptions are required, such as how often the data aggregation table is produced (in batch, or instantly when there's a change to the raw data table, amongst lots of other considerations). 

# Areas of improvement
- SQL connection repeated at each endpoint in `app/main.py` (14-15 and 42-43). I did this while developing as it was more important to get the core functionality working. It would've be nicer to abstract away the connection in a separate class or module. Unfortunately, I ran out of time to do this!