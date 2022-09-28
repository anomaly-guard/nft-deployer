from pyfift.core.contract_address import ContractAddress
from pyfift.core.boc import BoC
from pyfift.base.fift import Fift
from pyfift.base.app import App
from pyfift.core.state_init import StateInit


class WalletBase:
    def __init__(self) -> None:
        self.client = App.lite_client
        self.priv_key = App.key.priv_key
        self.address = type(self).address(App.key.pub_key)

    def seq_no(self) -> int:
        pass

    def pub_key(self) -> int:
        pass

    @classmethod
    def init_data(cls, pub_key: bytes | BoC = None):
        pass

    @classmethod
    def address(cls, pub_key: bytes | BoC = None):
        code = cls.code
        data = cls.init_data(pub_key or App.key.pub)
        init = StateInit(code, data).to_boc()
        addr = ContractAddress(init).human()
        return addr

    def build_message(self, sub_wallet: int, valid_until: int, seq_no: int, message: bytes | BoC):
        pass

    def transact(self, sub_wallet: int, valid_until: int, seq_no: int, message: bytes | BoC, message_mode: int = 64):
        msg, params = self.build_message(sub_wallet, valid_until, seq_no, message, message_mode=message_mode)
        outs = Fift().run(msg, params, ["result boc"])
        boc = outs["result boc"]
        return BoC(boc)
