import xml.etree.ElementTree as ET
from app.data import parse_xml

def test_parse_xml(xml_data):
    raw_data = ET.fromstring(xml_data)
    data = raw_data.findall('mcq-test-result')
    parse_data = parse_xml(data[0])
    assert type(parse_data) == dict
    assert parse_data["scanned_datetime"] == "2017-12-04T12:12:10+11:00"
    assert parse_data["student_number"] == "521585128"
    assert parse_data["test_id"] == "1234"
    assert parse_data["obtained_marks"] == "13"
    assert parse_data["available_marks"] == "20"
