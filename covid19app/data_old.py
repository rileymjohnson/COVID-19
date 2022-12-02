from montydb import MontyClient, MontyCursor, set_storage
from typing import Optional, List
from bson import ObjectId
import regex as re
import math


set_storage('db', cache_modified=5)
client = MontyClient('db')
db = client.cdc

def generate_search_regex(search_string, fields):
    if search_string is not None:
        search_regex = {
            '$regex': re.escape(search_string),
            '$options': 'i'
        }
        return {
            '$or': [{f: search_regex} for f in fields]
        }

    return {}

def get_document(_id):
    return db.documents.find_one({
        '_id': ObjectId(_id)
    })

def get_documents(
    *,
    k: Optional[int]=None,
    n: Optional[int]=None,
    search_string: Optional[str]=None,
    fields: List[str]=['title', 'document_slug', 'url']
) -> MontyCursor:
    query = generate_search_regex(search_string, fields)

    if n is not None:
        return db.documents.find(query, None, k * n, n)

    return db.documents.find(query)

def get_document_pages(
    n: int,
    search_string: Optional[str]=None,
    fields: List[str]=['title', 'document_slug', 'url']
) -> int:
    query = generate_search_regex(search_string, fields)
    num_documents = db.documents.count_documents(query)
    return math.ceil(num_documents / n)

def get_snapshot(_id):
    return db.snapshots.find_one({
        '_id': ObjectId(_id)
    })

def get_snapshots(
    *,
    k: Optional[int]=None,
    n: Optional[int]=None,
    search_string: Optional[str]=None,
    fields: List[str]=['title', 'document_slug', 'url']
) -> MontyCursor:
    query = generate_search_regex(search_string, fields)

    if n is not None:
        return db.snapshots.find(query, None, k * n, n)

    return db.snapshots.find(query)

def get_snapshot_pages(
    n: int,
    search_string: Optional[str]=None,
    fields: List[str]=['title', 'document_slug', 'url']
) -> int:
    query = generate_search_regex(search_string, fields)
    num_snapshots = db.snapshots.count_documents(query)
    return math.ceil(num_snapshots / n)

from mmap import mmap, ACCESS_READ
from pathlib import Path
import pandas as pd
import regex as re
import json


def search_documents(search_term: str) -> pd.DataFrame:
    regex_pattern = re.compile(
        search_term.encode(),
        re.DOTALL |
        re.IGNORECASE |
        re.MULTILINE
    )

    for file in Path('texts').glob('**/*.json'):
        with open(file, 'r') as f:
            with mmap(f.fileno(), 0, access=ACCESS_READ) as m:
                if regex_pattern.search(m):
                    for timestamp, data in json.loads(bytes(m)).items():
                        match_found = regex_pattern \
                            .search(data['text'].encode())

                        yield file, timestamp
