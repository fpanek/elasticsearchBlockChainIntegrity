import accessElastic

import logging
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

logging.basicConfig(
  format='%(asctime)s %(levelname)-8s %(message)s',
  level=logging.DEBUG,
  datefmt='%Y-%m-%d %H:%M:%S'
)


def start_hash_creation:
    query = {"bool": {"must_not": [{"exists": {"field": "integrity_checksum_created"}}]}}
    response = accessElastic.return_result_from_database("10.0.13.3", query, "example")
    for hit in response['hits']['hits']:
        print(hit)



