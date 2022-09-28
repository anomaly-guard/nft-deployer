import sys

from pyfift.base.app import App
from pyfift.wallet.wallet_v3_r2 import WalletV3R2
from pyfift.nft.nft_deploy import DeployNFTMessage



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
    print("insufficient balance for sending nft item message, min: 0.05 TON")
    sys.exit()


nft_collection_addr = "kQCtSPsG5JlnAeviQAzc811k2X4aRbHm1OJmzUnpkNNoPgLJ"
msg_body = DeployNFTMessage(
    index=0,
    content_url="my_nft.json",
    amount=50000000,
    owner=addr,
).to_boc()
wallet.send_to_contract(msg_body, 50000000, nft_collection_addr)