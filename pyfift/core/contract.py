from pyfift.base.app import App
from pyfift.core.code import ContractCode
from pyfift.core.state_init import StateInit
from pyfift.core.deploy_contract import DeployContract
from pyfift.core.contract_address import ContractAddress
from pyfift.wallet.wallet_base import WalletBase


class Contract:
    def init_code(self, code_path: str=None, code_hex: str=None):
        if code_path and code_hex:
            raise RuntimeError("Just one of code parameters can be specificed")
        if code_path:
            self.code = ContractCode(code_path).to_boc()
        if code_hex:
            self.code = code_hex
    
    def init_data(self, *args, **kwargs):
        self.data = None

    def address(self, binary=True):
        self.init = StateInit(self.code, self.data).to_boc()
        c = ContractAddress(self.init)
        self.addr = c.to_boc()
        self.h_addr = c.human()
        return self.addr if binary else self.h_addr

    def prepare_deploy(self, value: int = 0.01, external: bool = False, initial_msg=None):
        self.address()
        if initial_msg is None:
            initial_msg = self.initial_msg()
        self.msg = DeployContract(initial_msg, self.init, self.addr, App.key.priv_key, int(value * 10 ** 9)).to_boc(external=external)
        return self.msg
    
    def initial_msg(self):
        return None

    def deploy(self, wallet: WalletBase=None, sub_wallet=0, valid_until=-1, mode=64):
        if wallet:
            seq_no = wallet.seq_no()
            msg = wallet.transact(sub_wallet, valid_until, seq_no, self.msg, mode)
            s = App.lite_client.send_boc(msg)
            if s:
                print("Deploy message successfully sent to lite-servers!")
        else:
            # Direct deploy
            App.lite_client.send_boc(self.msg)
