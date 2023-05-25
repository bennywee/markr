from flask import Flask, request, Response
import xml.etree.ElementTree as ET
import sqlite3

from data import parse_xml

app = Flask(__name__)

@app.route("/import/", methods=['POST'])
def extract_load_xml():
    xml_data = request.data
    db_conn = sqlite3.connect("db/markr.db")
    cur = db_conn.cursor()
    
    insert_query = """
    INSERT INTO results VALUES (
        :created_datetime,
        :updated_datetime, 
        :scanned_datetime,
        :student_number,
        :test_id,
        :obtained_marks,
        :available_marks)
    ON CONFLICT(student_number, test_id)
    DO UPDATE SET 
        obtained_marks = MAX(obtained_marks, excluded.obtained_marks),
        available_marks = MAX(available_marks, excluded.available_marks),
        updated_datetime = excluded.updated_datetime
    """
        
    raw_data = ET.fromstring(xml_data)
    data = tuple(parse_xml(result) for result in raw_data.findall('mcq-test-result'))
    cur.executemany(insert_query, data)
    db_conn.commit()
    db_conn.close()
    return Response("Data uploaded successfully")

@app.route("/results/<test_id>/aggregate", methods=['GET'])
def summary_stats(test_id: str) -> dict:
    ...

if __name__ == "__main__":
   app.run(port=4567)