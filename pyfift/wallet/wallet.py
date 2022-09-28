from pyfift.base.app import App
from pyfift.core.boc import BoC
from pyfift.wallet._wallet_base import WalletBase
from pyfift.wallet._wallet_v3_r2 import WalletV3R2
from pyfift.wallet._wallet_v4 import WalletV4


class Wallet:
    bases = {
        3: WalletV3R2,
        4: WalletV4
    }
    base: WalletBase
    def __init__(self, version: int = 3) -> None:
        self.base = Wallet.bases[version]()

    @classmethod
    def address(cls, pub_key: str = None, version: int = 3):
        pub_key = pub_key or App.key.pub_key
        return Wallet.bases[version].address(pub_key)

    @classmethod
    def init_data(cls, pub_key: str = None, version: int = 3):
        pub_key = pub_key or App.key.pub_key
        return Wallet.bases[version].init_data(pub_key)

    def build(self, sub_wallet: int = 0, valid_until: int = -1, seq_no: int = -1, message: bytes | BoC = None, message_mode: int = 64):
        return self.base.transact(sub_wallet, valid_until, seq_no, message, message_mode)