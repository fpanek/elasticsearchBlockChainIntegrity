import solcx
import warnings
from solcx import compile_standard, install_solc
from web3 import Web3

warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')

install_solc('0.8.0')

with open("SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)

# Get bytecode and ABI
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Ensure the connection is successful
if not w3.is_connected():
    raise Exception("Failed to connect to Ganache")

# Set the default account (the first account in Ganache)
w3.eth.default_account = w3.eth.accounts[0]

# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

#tx_hash = SimpleStorage.constructor().transact({'from': w3.eth.default_account})

#tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

#contract_address = tx_receipt.contractAddress
#print(f"Contract deployed at address: {contract_address}")

#simple_storage = w3.eth.contract(address=contract_address, abi=abi)

simple_storage = w3.eth.contract(address="0xec3Cca6797DDf89b03Be3776EF90b5503D52B3fa", abi=abi)

# Set a value
tx_hash = simple_storage.functions.set(32).transact({'from': w3.eth.default_account})
w3.eth.wait_for_transaction_receipt(tx_hash)

# Get the value
stored_data = simple_storage.functions.get().call()
print(f"Stored data: {stored_data}")
