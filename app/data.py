from datetime import datetime, timezone

def parse_xml(data) -> dict:
    data_dict = {
    "created_datetime": datetime.utcnow().replace(tzinfo=timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f'),
    "updated_datetime": datetime.utcnow().replace(tzinfo=timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f'),
    "scanned_datetime": data.attrib['scanned-on'],
    "student_number": data.find('student-number').text,
    "test_id": data.find('test-id').text,
    "obtained_marks": next(data.iter('summary-marks')).attrib['obtained'],
    "available_marks": next(data.iter('summary-marks')).attrib['available']
    }
    return data_dict