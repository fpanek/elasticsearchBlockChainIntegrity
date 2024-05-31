import logging

import accessElastic
from datetime import datetime, timezone
import random
import string
import time

import config.config as config

AmountOfDocumentsToTamper=10
index_to_tamper="example4"


if __name__ == '__main__':
    current_time = datetime.now(timezone.utc)
    start_time = time.time()
    query = {
        "query": {
            "function_score": {
                "query": {"match_all": {}},
                "functions": [
                    {
                        "random_score": {}
                    }
                ],
                "boost_mode": "replace"
            }
        }
    }
    tamperDocuments = accessElastic.return_limited_result_from_database(config.database_ip, query, index_to_tamper, AmountOfDocumentsToTamper)
    for hit in tamperDocuments['hits']['hits']:
        for hit in tamperDocuments['hits']['hits']:
            document_id = hit['_id']
            print(document_id)
            document_body = {
                "content": f"tampered data {''.join(random.choices(string.digits, k=5))}"
            }
            accessElastic.update_document(config.database_ip, index_to_tamper, document_id, document_body)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"Tampering {AmountOfDocumentsToTamper} Documents took {elapsed_time} seconds")


