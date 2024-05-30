import warnings
from web3 import Web3

warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

if not w3.is_connected():
    raise Exception("Failed to connect to Ganache")

abi = [
    {
        "inputs": [],
        "name": "get",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "x",
                "type": "uint256"
            }
        ],
        "name": "set",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

contract_address = 'YOUR_CONTRACT_ADDRESS_HERE'  # Replace with the actual contract address

# Interact with the deployed contract
simple_storage = w3.eth.contract(address="0xec3Cca6797DDf89b03Be3776EF90b5503D52B3fa", abi=abi)

# Retrieve the stored value
stored_data = simple_storage.functions.get().call()
print(f"Stored data: {stored_data}")
