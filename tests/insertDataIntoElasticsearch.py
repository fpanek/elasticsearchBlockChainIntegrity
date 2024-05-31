import logging

import accessElastic
from datetime import datetime, timezone
import random
import string
import time
def insert_test_document(index, document_body):
    response = accessElastic.insert_document("10.0.13.3", index, "", document_body)
    print(response)


documentsToInsert=400
index_to_insert="example4"


if __name__ == '__main__':
    current_time = datetime.now(timezone.utc)
    timestamp = current_time.isoformat(timespec='seconds').replace('+00:00', 'Z')
    start_time = time.time()
    for i in range(documentsToInsert):
        document_body = {
            "@timestamp": timestamp,
            "title": ''.join(random.choices(string.ascii_letters, k=5)),
            "content": f"Test insert {i} {''.join(random.choices(string.ascii_letters, k=10))}"
        }
        insert_test_document(index_to_insert, document_body)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"Inserting {documentsToInsert} Documents took {elapsed_time} seconds")


