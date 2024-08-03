import json
from solcx import compile_standard, install_solc
from web3 import Web3

install_solc('0.8.0')

with open('MyNFT.sol', 'r') as file:
    my_nft_source = file.read()

compiled_sol = compile_standard({
    'language': 'Solidity',
    'sources': {
        'MyNFT.sol': {
            'content': my_nft_source
        }
    },
    'settings': {
        'outputSelection': {
            '*': {
                '*': ['abi', 'metadata', 'evm.bytecode', 'evm.sourceMap']
            }
        }
    }
}, solc_version='0.8.0')

with open('compiled_code.json', 'w') as file:
    json.dump(compiled_sol, file)

w3 = Web3(Web3.HTTPProvider('https://rinkeby.infura.io/v3/YOUR_INFURA_PROJECT_ID'))
chain_id = 4
my_address = 'YOUR_ETH_ADDRESS'
private_key = 'YOUR_PRIVATE_KEY'

bytecode = compiled_sol['contracts']['MyNFT.sol']['MyNFT']['evm']['bytecode']['object']
abi = json.loads(compiled_sol['contracts']['MyNFT.sol']['MyNFT']['metadata'])['output']['abi']

MyNFT = w3.eth.contract(abi=abi, bytecode=bytecode)

transaction = MyNFT.constructor('ipfs://YOUR_BASE_TOKEN_URI/').buildTransaction({
    'chainId': chain_id,
    'gas': 7000000,
    'gasPrice': w3.toWei('21', 'gwei'),
    'nonce': w3.eth.getTransactionCount(my_address),
})

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(f'Contract deployed at address: {tx_receipt.contractAddress}')
