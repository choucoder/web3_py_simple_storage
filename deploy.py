import json
from solcx import compile_standard, install_solc
from web3 import Web3
from decouple import config


with open('SimpleStorage.sol', 'r') as f:
    contract_data = f.read()
    print(contract_data)

install_solc('0.8.1')

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": contract_data}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        }
    },
    solc_version="0.8.1"
)

with open('compiled_code.json', 'w') as f:
    json.dump(compiled_sol, f)


# Get the bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# Get the abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]


# Connecting to ganache

w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/f1e6febcbb80484d89d2345c18d014c6"))
chain_id = 4
my_address = "0x3D2659882a70421498E8953A662dDdd95591Be77"
private_key = config('PRIVATE_KEY')

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latestest transaction
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)
# Build a transaction
transaction = SimpleStorage.constructor().buildTransaction({"gasPrice": w3.eth.gas_price, "chainId": chain_id, "from": my_address, "nonce": nonce})
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

print("Deploying contract...")
# Send the signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")

# Working with the contract
# Contract Address
# Contract ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Call -> Simulate making the call and getting a return value
# Transact -> Actually make a state change

# Initial value of favorite number
print(simple_storage.functions.retrieve().call())

print("Updating contract...")
store_transaction = simple_storage.functions.store(22).buildTransaction(
    {"gasPrice": w3.eth.gas_price, "chainId": chain_id, "from": my_address, "nonce": nonce + 1}
)

signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

send_store_txn = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_txn)
print("Updated!")

print(simple_storage.functions.retrieve().call())
