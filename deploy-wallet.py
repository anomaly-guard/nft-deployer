from pyfift.base.app import App
from pyfift.wallet.wallet_v3_r2 import WalletV3R2


App.init()

wallet = WalletV3R2()
wallet.init_data()
addr = wallet.address(binary=False)
state = App.lite_client.state(addr)
if state["state"] == "empty":
    print("This account is fresh ...")
    print("Wallet Address:", addr)
    print("Please send some TONs to the address to deploy it later")
elif state["state"] == "active":
    print("This account is already active and deployed ...")
    print("Wallet Address:", addr)
    print("Balance: %.5f TON" % (state["balance"] / (10 ** 9)))
elif state["state"] == "inactive":
    min_balance = 50000000 # .05 TONs
    if state["balance"] < min_balance:
        print("Please send at least 0.2TONs to proceed for deployment ...")
    print("This account is inactive and ready to deploy wallet contract")
    wallet.prepare_deploy(value=0, external=True)
    wallet.deploy()
