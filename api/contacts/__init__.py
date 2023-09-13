from typing import List

from config import config


def is_valid_file_csv_type(content_type: str):
    return content_type == "text/csv"


def is_valid_csv_columns(csv_columns: List[str]):
    return config.MANDATORY_HEADERS.issubset(set(csv_columns))


def get_csv_headers(csv_reader):
    csv_headers = []
    for row in csv_reader:
        csv_headers = row.copy()
        return csv_headers
    return []


def process_csv_file(csv_reader):
    for row in csv_reader:
        print(row)


# def connect_db
