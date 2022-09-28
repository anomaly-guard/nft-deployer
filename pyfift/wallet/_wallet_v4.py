from pyfift.wallet._wallet_base import WalletBase


class WalletV4(WalletBase):
    code = ""
    
    def pub_key(self) -> int:
        o = self.client.get_method(78748, self.address)
        return int(o.strip())

    def seq_no(self) -> int:
        o = self.client.get_method(85143, self.address)
        return int(o.strip())
