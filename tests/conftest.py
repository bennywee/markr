import sqlite3

import pytest

from app.main import app as flask_app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db():
    db = sqlite3.connect(":memory:")
    cur = db.cursor()

    ddl_query = """
    CREATE TABLE IF NOT EXISTS results (
    created_datetime TEXT NOT NULL,
    updated_datetime TEXT NOT NULL,
    scanned_datetime TEXT NOT NULL,
    student_number TEXT NOT NULL, 
    test_id TEXT NOT NULL,
    obtained_marks INT,
    available_marks INT,
    PRIMARY KEY (student_number, test_id)
    )
    """

    dml_query = """
    INSERT INTO results VALUES
    ('2023-02-25T01:07:00.000000', '2023-10-25T10:07:00.000000', '2017-12-04T12:12:10+11:00', '5585128', '9000', 10, 20),  
    ('2023-01-25T01:07:00.000000', '2023-10-25T10:07:00.000000', '2017-12-04T12:12:10+11:00', '2299', '9000', 12, 20), 
    ('2023-03-15T01:07:00.000000', '2023-10-25T10:07:00.000000', '2017-12-04T12:13:10+11:00', '2300', '9000', 1, 20), 
    ('2023-02-29T01:07:00.000000', '2023-10-25T10:07:00.000000', '2017-12-04T12:14:10+11:00', '2304', '9000', 20, 20)
    """

    cur.execute(ddl_query)
    cur.execute(dml_query)

    return db


@pytest.fixture
def xml_data():
    xml_string = """
    <mcq-test-results>
        <mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
            <first-name>Jane</first-name>
            <last-name>Austen</last-name>
            <student-number>521585128</student-number>
            <test-id>1234</test-id>
            <summary-marks available="20" obtained="13" />
        </mcq-test-result>
    </mcq-test-results>
    """

    return xml_string


@pytest.fixture
def missing_data():
    """
    Missing critical data field
    """

    xml_string = """
    <mcq-test-results>
        <mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
            <first-name>Jane</first-name>
            <last-name>Austen</last-name>
            <student-number>521585128</student-number>
            <summary-marks available="20" obtained="13" />
        </mcq-test-result>
    </mcq-test-results>
    """

    return xml_string


@pytest.fixture
def invalid_data():
    """
    Incorrect XML format
    """

    xml_string = """
    <mcq-test-results>
            <first-name>Jane</first-name>
            <last-name>Austen</last-name>
            <student-number>521585128</student-number>
            <test-id>1234</test-id>
            <summary-marks available="20" obtained="13" />
        </mcq-test-result>
    </mcq-test-results>
    """

    return xml_string


@pytest.fixture
def scores_as_strings():
    """
    Scores as strings instead of integers
    """

    xml_string = """
    <mcq-test-results>
            <first-name>Jane</first-name>
            <last-name>Austen</last-name>
            <student-number>521585128</student-number>
            <test-id>1234</test-id>
            <summary-marks available="abc" obtained="xyz" />
        </mcq-test-result>
    </mcq-test-results>
    """

    return xml_string
