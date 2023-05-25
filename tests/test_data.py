import pytest
import xml.etree.ElementTree as ET

from app.data import parse_xml

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

def test_parse_xml(xml_data):
    raw_data = ET.fromstring(xml_data)
    data = parse_xml(result) for result in raw_data.findall('mcq-test-result')
    ...
    assert type(data) == dict
