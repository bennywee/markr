from flask import Flask, request, Response
import xml.etree.ElementTree as ET
import sqlite3

app = Flask(__name__)

@app.route("/import/", methods=['POST'])
def extract_load_xml():
    ...

@app.route("/results/<test_id>/aggregate", methods=['GET'])
def summary_stats(test_id: str) -> dict:
    ...