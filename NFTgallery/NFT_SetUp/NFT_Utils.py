from web3 import Web3
import json


w3 = Web3(Web3.HTTPProvider('https://rinkeby.infura.io/v3/YOUR_INFURA_PROJECT_ID'))
my_address = 'YOUR_ETH_ADDRESS'
private_key = 'YOUR_PRIVATE_KEY'


contract_address = 'YOUR_DEPLOYED_CONTRACT_ADDRESS'
with open('compiled_code.json', 'r') as file:
    compiled_sol = json.load(file)
abi = json.loads(compiled_sol['contracts']['MyNFT.sol']['MyNFT']['metadata'])['output']['abi']

nft_contract = w3.eth.contract(address=contract_address, abi=abi)


def upload_photo(request, photo):
    # if form.is_valid():
    #     photo = form.save()
    image_url = request.build_absolute_uri(photo.image.url)

    transaction = nft_contract.functions.mintTo(my_address).buildTransaction({
        'chainId': 4,
        'gas': 700000,
        'gasPrice': w3.toWei('21', 'gwei'),
        'nonce': w3.eth.getTransactionCount(my_address),
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    token_id = nft_contract.functions.nextTokenId().call() - 1

    # photo.nft_token = token_id
    # photo.save()
    return token_id
