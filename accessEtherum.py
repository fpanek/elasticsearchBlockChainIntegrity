import config
from web3 import Web3
from solcx import compile_standard, install_solc
import os

import logging
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

logging.basicConfig(
  format='%(asctime)s %(levelname)-8s %(message)s',
  level=logging.DEBUG,
  datefmt='%Y-%m-%d %H:%M:%S'
)

def iterate_through_all_blocks():
    ganache_path = f"http://{config.etherum_node_ip}:{config.etherum_node_port}"
    etherum_client = Web3(Web3.HTTPProvider(ganache_path))

    if etherum_client.is_connected():
        logging.debug("Etherum client is connected :)")
    else:
        logging.error("Error conneecting to etherum node")

    latest_block = etherum_client.eth.block_number
    print(f"Latest block number: {latest_block}")

    for block_number in range(latest_block + 1):
        block = etherum_client.eth.get_block(block_number)
        print(f"Block {block_number}: Hash - {block['hash'].hex()}")

def compile_and_deploy(smart_contract_file):
    install_solc('0.8.0')
    ganache_path = f"http://{config.etherum_node_ip}:{config.etherum_node_port}"
    w3 = Web3(Web3.HTTPProvider(ganache_path))
    with open(smart_contract_file, 'r') as file:
        contract_source_code = file.read()
    contract_name = os.path.basename(smart_contract_file).split('.')[0]
    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {smart_contract_file: {"content": contract_source_code}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        }
    }, solc_version='0.8.0')

    bytecode = compiled_sol['contracts'][smart_contract_file][contract_name]['evm']['bytecode']['object']
    abi = compiled_sol['contracts'][smart_contract_file][contract_name]['abi']

    Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    account = w3.eth.accounts[0]  # typically the first account is used for deployment

    tx_hash = Contract.constructor().transact({'from': account})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)


def verify_contract(address):
    ganache_path = f"http://{config.etherum_node_ip}:{config.etherum_node_port}"
    w3 = Web3(Web3.HTTPProvider(ganache_path))
    return w3.eth.contract(address=address, abi=abi)

def set_key_value(contract, key, value):
    tx_hash = contract.functions.set(key, value).transact()
    w3.eth.wait_for_transaction_receipt(tx_hash)

def get_value(contract, key):
    return contract.functions.get(key).call()