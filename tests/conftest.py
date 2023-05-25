import sys
sys.path.append('/markr/app/')

import pytest
import sqlite3
from app.main import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db():
    db = sqlite3.connect(':memory:')
    query = """
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
    db.execute(query)
    yield db

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
            <test-id>1234</test-id>
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