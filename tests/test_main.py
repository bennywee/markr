from unittest.mock import MagicMock, patch


def test_extract_load_missing(client, db, missing_data):
    with patch("sqlite3.connect", MagicMock(return_value=db)):
        missing_response = client.post("/import/", data=missing_data)
        assert missing_response.status_code == 400


def test_extract_load_invalid(client, db, invalid_data):
    with patch("sqlite3.connect", MagicMock(return_value=db)):
        invalid_response = client.post("/import/", data=invalid_data)
        assert invalid_response.status_code == 400


def test_extract_load_score_strings(client, db, scores_as_strings):
    with patch("sqlite3.connect", MagicMock(return_value=db)):
        string_response = client.post("/import/", data=scores_as_strings)
        assert string_response.status_code == 400


def test_extract_load_xml(db, client, xml_data):
    with patch("sqlite3.connect", MagicMock(return_value=db)):
        response = client.post("/import/", data=xml_data)
        assert response.status_code == 200


def test_summary_stats_error(db, client):
    with patch("sqlite3.connect", MagicMock(return_value=db)):
        bad_response = client.get("/results/1/aggregate")
        assert bad_response.status_code == 400


def test_summary_stats(db, client):
    with patch("sqlite3.connect", MagicMock(return_value=db)):
        good_response = client.get("/results/9000/aggregate")
        assert good_response.status_code == 200
