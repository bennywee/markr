import itertools
import sqlite3
import xml.etree.ElementTree as ET

from data import parse_xml, stats
from flask import Flask, Response, request

app = Flask(__name__)


@app.route("/import/", methods=["POST"])
def extract_load_xml():
    xml_data = request.data
    db_conn = sqlite3.connect("db/markr.db")
    cur = db_conn.cursor()

    with open("app/insert.sql", "r") as sql_dml:
        insert_query = sql_dml.read()

    try:
        raw_data = ET.fromstring(xml_data)
        data = tuple(
            parse_xml(result) for result in raw_data.findall("mcq-test-result")
        )
        cur.executemany(insert_query, data)
        db_conn.commit()
        db_conn.close()
        return Response("Data uploaded successfully", status=200)
    except ET.ParseError:
        return Response("400 Bad request: Invalid XML data", status=400)
    except (RuntimeError, AttributeError):
        db_conn.rollback()
        db_conn.close()
        return Response("400 Bad request: Document missing important data", status=400)


@app.route("/results/<test_id>/aggregate", methods=["GET"])
def summary_stats(test_id: str) -> dict:
    with open("app/test_scores.sql", "r") as sql_scores:
        scores_query = sql_scores.read()

    db_conn = sqlite3.connect("db/markr.db")
    cur = db_conn.cursor()
    percentages = cur.execute(scores_query, {"test_id": test_id}).fetchall()
    percentages_list = list(itertools.chain(*percentages))

    if len(percentages_list) > 0:
        test_scores = stats(scores=percentages_list)
        db_conn.close()
        return test_scores
    else:
        db_conn.close()
        return Response("400 Bad request: Test id does not exist", status=400)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
