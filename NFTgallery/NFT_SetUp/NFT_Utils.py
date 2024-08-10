import ipfshttpclient
from rest_framework.serializers import Serializer
from web3 import Web3
#
from .vars import ABI, PRIVATE_KEY
#


def create_nft(image_path):
    # اتصال به IPFS
    print('zero \n' * 10)
    client = ipfshttpclient.connect()
    res = client.add(image_path)
    ipfs_uri = f"ipfs://{res['Hash']}"
    print('one \n' * 10)

    # اتصال به اتریوم
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/1ffebe271bd04a399f9f63444d487b2e'))
    account = w3.eth.account.privateKeyToAccount(PRIVATE_KEY)
    contract_address = '0xf8e81D47203A594245E36C48e151709F0C19fBe8'
    abi = ABI
    contract = w3.eth.contract(address=contract_address, abi=abi)
    print('two \n' * 10)

    # ایجاد تراکنش برای ساخت NFT
    tx = contract.functions.createToken(ipfs_uri).buildTransaction({
        'from': account.address,
        'nonce': w3.eth.getTransactionCount(account.address),
        'gas': 2000000,
        'gasPrice': w3.toWei('50', 'gwei')
    })
    print('three \n' * 10)

    signed_tx = w3.eth.account.signTransaction(tx, private_key=account.privateKey)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print('four \n' * 10)
    return w3.toHex(tx_hash)

# داخل ImageUploadView و بعد از ذخیره تصویر
# if serializer.is_valid():
#     instance = serializer.save()
#     tx_hash = create_nft(instance.image.path)
#     # انجام کارهای بیشتر با tx_hash اگر لازم باشد
#     return Response(serializer.data, status=status.HTTP_201_CREATED)
