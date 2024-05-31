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


def verify_integrity(index_name):
    contract = load_contract(Web3.to_checksum_address(config.existing_contract_address), "abi.json")
    _id = "QcnQzY8BV3C7FM5l190G"
    result = accessEtherum.get_checksum_entry(contract, index_name, _id)
    logging.debug(f"Found checksum: {result} in index: {index_name} for _id: {_id}")
    #get_single_checksum_entry(contract, "example", "KcnhtY8BV3C7FM5lft27")
    #get_all_checksums(contract, index_name)


