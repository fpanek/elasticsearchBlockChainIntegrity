import logging
import warnings
from solcx import compile_standard, install_solc
from web3 import Web3
import config
import json

warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')
warnings.filterwarnings("ignore", category=DeprecationWarning)

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S'
)

ganache_path = f"http://{config.etherum_node_ip}:{config.etherum_node_port}"
CONTRACT_FILE = "DocumentIntegrity.sol"
SOLC_VERSION = "0.8.13"

w3 = Web3(Web3.HTTPProvider(ganache_path))
if not w3.is_connected():
    raise Exception("Failed to connect to Ganache")

DEPLOYER_ACCOUNT = w3.eth.accounts[0]

def compile_contract(contract_file, solc_version):
    install_solc(solc_version)
    with open(contract_file, 'r') as file:
        contract_source_code = file.read()
    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {contract_file: {"content": contract_source_code}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.deployedBytecode"]
                }
            }
        }
    }, solc_version=solc_version)
    contract_name = contract_file.split('.')[0]
    bytecode = compiled_sol['contracts'][contract_file][contract_name]['evm']['bytecode']['object']
    abi = compiled_sol['contracts'][contract_file][contract_name]['abi']
    with open('abi.json', 'w') as abi_file:
        json.dump(abi, abi_file)
    return bytecode, abi

def format_address(address):
    return Web3.to_checksum_address(address)

def get_deployed_bytecode(contract_address):
    formatted_address = format_address(contract_address)
    return w3.eth.get_code(formatted_address)

def contains_bytecode(full_bytecode, deployed_bytecode):
    if not deployed_bytecode or deployed_bytecode not in full_bytecode:
        return False
    return True

def deploy_smart_contract(bytecode, abi):
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.get_transaction_count(DEPLOYER_ACCOUNT)
    transaction = contract.constructor().build_transaction({
        'chainId': w3.eth.chain_id,
        'gas': 2000000,
        'gasPrice': Web3.to_wei('20', 'gwei'),
        'nonce': nonce,
        'from': DEPLOYER_ACCOUNT
    })
    tx_hash = w3.eth.send_transaction(transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt['contractAddress']


def update_contract_address(new_address):
    config_file_path = 'config.py'
    with open(config_file_path, 'r') as file:
        lines = file.readlines()
    address_updated = False
    for i in range(len(lines)):
        if 'existing_contract_address' in lines[i]:
            new_line = f'existing_contract_address = "{new_address}"  # Updated address\n'
            if lines[i].strip() != new_line.strip():
                lines[i] = new_line
            address_updated = True
            break
    if not address_updated:
        lines.append(f'existing_contract_address = "{new_address}"  # Updated address\n')
    with open(config_file_path, 'w') as file:
        file.writelines(lines)



def verify_and_deploy_smart_contract():
    logging.debug("Start compilation of bytecode")
    compiled_bytecode, abi = compile_contract(CONTRACT_FILE, SOLC_VERSION)
    contract_address = config.existing_contract_address
    if contract_address:
        logging.debug("Get deployed bytecode from blockchain")
        deployed_bytecode_to_compare = get_deployed_bytecode(contract_address).hex()[2:]  # Remove '0x' for comparison
        compiled_bytecode_to_compare = compiled_bytecode[2:]  # Remove '0x' from compiled bytecode for consistency for comparisn
        if contains_bytecode(compiled_bytecode_to_compare, deployed_bytecode_to_compare):
            logging.debug(f"{compiled_bytecode_to_compare}")
            logging.debug(f"{deployed_bytecode_to_compare}")
            logging.debug("The deployed contract contains the compiled bytecode. - no action required...")
            return contract_address
        else:
            logging.info("Bytecode mismatch or empty deployed bytecode. Deploying the latest version...")
            new_contract_address = deploy_smart_contract(compiled_bytecode, abi)
            logging.info(f"New contract deployed at address: {new_contract_address}")
            update_contract_address(new_contract_address)
    else:
        logging.info("No deployed contract address provided. Deploying new contract...")
        new_contract_address = deploy_smart_contract(compiled_bytecode, abi)
        logging.info(f"New contract deployed at address: {new_contract_address}")
        update_contract_address(new_contract_address)
        return new_contract_address

