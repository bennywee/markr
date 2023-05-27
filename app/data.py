from datetime import datetime, timezone

import numpy as np


def parse_xml(data) -> dict:
    data_dict = {
        "created_datetime": datetime.utcnow()
        .replace(tzinfo=timezone.utc)
        .strftime("%Y-%m-%dT%H:%M:%S.%f"),
        "updated_datetime": datetime.utcnow()
        .replace(tzinfo=timezone.utc)
        .strftime("%Y-%m-%dT%H:%M:%S.%f"),
        "scanned_datetime": data.attrib["scanned-on"],
        "student_number": data.find("student-number").text,
        "test_id": data.find("test-id").text,
        "obtained_marks": next(data.iter("summary-marks")).attrib["obtained"],
        "available_marks": next(data.iter("summary-marks")).attrib["available"],
    }
    return data_dict


def stats(scores: list) -> dict:
    mean = np.round(np.mean(scores), 1)
    std = np.round(np.std(scores), 1)
    p25 = np.percentile(scores, 25)
    p50 = np.percentile(scores, 50)
    p75 = np.percentile(scores, 75)
    count = len(scores)

    summary_statistics = {
        "mean": mean,
        "std": std,
        "p25": p25,
        "p50": p50,
        "p75": p75,
        "count": count,
    }

    return summary_statistics
