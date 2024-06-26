import accessElastic

import logging
import json
import accessEtherum
import config.config as config
import createChecksum
from web3 import Web3
import accessElastic
from datetime import datetime
import os

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

def query_specific_index_and_id(ip, index, _id):
    body = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"_id": _id}}
                ]
            }
        },
        "size": 1  # Limit the number of search results to only one document
    }
    response = accessElastic.return_result_from_database_using_body(ip, body, index)
    return response


def write_integrity_report(index, _id, timestamp, title, content):
    integrityReport = config.integrityReport
    json_data = {
        "date": timestamp.strftime("%Y-%m-%d-%H-%M-%S"),
        "index": index,
        "_id": _id,
        "title": title,
        "content": content
    }
    comparison_data = {k: v for k, v in json_data.items() if k != "date"}
    if os.path.exists(integrityReport):
        with open(integrityReport, 'r') as file:
            existing_entries = [json.loads(line.strip()) for line in file]
        existing_entries = [
            {k: v for k, v in entry.items() if k != "date"} for entry in existing_entries
        ]
    else:
        existing_entries = []
    if not any(
        json.dumps(comparison_data, sort_keys=True) == json.dumps(entry, sort_keys=True) for entry in existing_entries):
        with open(integrityReport, 'a') as file:
            json_string = json.dumps(json_data)
            file.write(json_string + '\n')


def verify_integrity(index_name):
    contract = load_contract(Web3.to_checksum_address(config.existing_contract_address), "../config/abi.json")
    data = accessEtherum.get_all_checksums(contract, index_name)
    results = []
    for i in range(len(data[0])):
        results.append({"_id": data[0][i], "checksum": data[1][i]})
    blockhain_checksum_id = json.dumps({"results": results}, indent=4)
    blockhain_checksum_id_json = json.loads(blockhain_checksum_id)
    for item in blockhain_checksum_id_json['results']:
        _id = item['_id']
        checksum_blockchain = item['checksum']
        elastic_result = query_specific_index_and_id("10.0.13.3", index_name, _id)
        #print("-------elastic result")
        #print(elastic_result)
        if elastic_result['hits']['hits']:  # Check if there are hits
            first_hit = elastic_result['hits']['hits'][0]['_source']
            timestamp = first_hit['@timestamp']
            title = first_hit['title']
            content = first_hit['content']
            logging.debug(f"Got result: timestamp:{timestamp}, title: {title}, content:{content}")
            logging.debug(f"Creating checksum: timestamp:{timestamp}, title: {title}, content:{content}")
            checksum_elastic = createChecksum.create_checksum(timestamp, title, content)
            logging.info(f"Checksum Blockchain {checksum_blockchain}; Checksum Elastic: {checksum_elastic}")
            if checksum_blockchain == checksum_elastic:
                logging.debug("checksum equal OK")
            else:
                logging.error(f"Document {_id} was altered after creating the checksum!")
                current_timestamp = datetime.now()
                write_integrity_report(index_name, _id, current_timestamp, title, content)
        else:
            logging.debug("Error decoding document")







