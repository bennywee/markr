from unittest.mock import patch, MagicMock

def test_extract_load_xml_error(client, missing_data, invalid_data):
    mising_response = client.post('/import/', data = missing_data)
    invalid_response = client.post('/import/', data = invalid_data)
    assert mising_response.status_code == 400
    assert invalid_response.status_code == 400

def test_extract_load_xml(db, client, xml_data):
    with patch('sqlite3.connect', MagicMock(return_value=db)):
        response = client.post('/import/', data = xml_data)
        assert response.status_code == 200

