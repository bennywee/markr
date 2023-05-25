import xml.etree.ElementTree as ET

from app.data import parse_xml, stats


def test_parse_xml(xml_data):
    raw_data = ET.fromstring(xml_data)
    data = raw_data.findall("mcq-test-result")
    parse_data = parse_xml(data[0])
    assert type(parse_data) == dict
    assert parse_data["scanned_datetime"] == "2017-12-04T12:12:10+11:00"
    assert parse_data["student_number"] == "521585128"
    assert parse_data["test_id"] == "1234"
    assert parse_data["obtained_marks"] == "13"
    assert parse_data["available_marks"] == "20"


def test_stats():
    data = [1, 2, 3, 4, 5]
    results = stats(data)
    assert type(results) == dict
    assert results["mean"] == 3.0
    assert results["std"] == 1.4
    assert results["p25"] == 2
    assert results["p50"] == 3
    assert results["p75"] == 4
    assert results["count"] == 5
