import accessElastic

import logging
import json
import accessEtherum
import config
import createChecksum
from web3 import Web3


logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

logging.basicConfig(
  format='%(asctime)s %(levelname)-8s %(message)s',
  level=logging.DEBUG,
  datefmt='%Y-%m-%d %H:%M:%S'
)

ganache_path = f"http://{config.etherum_node_ip}:{config.etherum_node_port}"
w3 = Web3(Web3.HTTPProvider(ganache_path))
def load_contract(contract_address, abi_path):
    with open(abi_path, 'r') as abi_file:
        abi = json.load(abi_file)
    return w3.eth.contract(address=contract_address, abi=abi)

def create_and_store_hash():
    query = {"bool": {"must_not": [{"exists": {"field": "integrity_checksum_created"}}]}}
    response = accessElastic.return_result_from_database("10.0.13.3", query, "example")
    for hit in response['hits']['hits']:
        document_id = hit['_id']  # Extract the document ID
        timestamp=hit['_source']['@timestamp']
        title=hit['_source']['title']
        content=hit['_source']['content']
        logging.debug(f"found document: {document_id} {timestamp}; {title}; {content}")
        checksum = createChecksum.create_checksum(timestamp, title, content)
        contract=load_contract(Web3.to_checksum_address(config.existing_contract_address), "config/abi.json")
        accessEtherum.add_checksum_entry(contract, "example", document_id, checksum)
        document_already_read = {
        "integrity_checksum_created": True
        }
        accessElastic.update_document("10.0.13.3", "example", document_id, document_already_read)


