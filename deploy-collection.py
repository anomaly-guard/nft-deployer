import sys

from pyfift.base.app import App
from pyfift.wallet.wallet_v3_r2 import WalletV3R2
from pyfift.nft.nft_collection import NftCollection


App.init()

wallet = WalletV3R2()
wallet.init_data()
addr = wallet.address(binary=False)
state = App.lite_client.state(addr)

if state["state"] != "active":
    if state["state"] == "empty": print("Empty account, send some TONs and deploy it ...")
    elif state["state"] == "inactive": print("Deploy the wallet contract before proceeding ...")
    sys.exit()

if state["balance"] < 50000000:
    print("insufficient balance for deploying nft contract, min: 0.05 TON")
    sys.exit()

collection = NftCollection()
collection.init_data(
    addr,
    5, 100, 0,
    'https://raw.githubusercontent.com/ton-blockchain/token-contract/main/nft/web-example/my_collection.json',
    'https://raw.githubusercontent.com/ton-blockchain/token-contract/main/nft/web-example/'
)
collection.prepare_deploy(value=0.05, external=False)
print("preparing to deploy nft collection contract ...")
print("NFT Collection address:", collection.h_addr)
collection.deploy(wallet, mode=64 + 3)