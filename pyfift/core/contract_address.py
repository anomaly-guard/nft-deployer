from pyfift.base.app import App
from pyfift.base.fift import Fift
from pyfift.core.boc import BoC

class ContractAddress:
    build_contract_address = '''
        "Asm.fif" include
        "TonUtil.fif" include
        B{%state_init%} B>boc
        constant state_init
        0 constant work_chain
        state_init hashu constant state_hash
        // Contract Address
        <b 4 3 u, work_chain 8 i, state_hash 256 u, b> constant addr_cell
        addr_cell 2 boc+>B constant b_addr

        work_chain state_hash %network_mode_flag% smca>$ constant h_addr

        "result boc:{" type b_addr Bx. "}" type
        "human readable:{" type h_addr type "}" type
        '''

    # _ split_depth:(Maybe (## 5)) special:(Maybe TickTock)
    #   code:(Maybe ^Cell) data:(Maybe ^Cell)
    #   library:(HashmapE 256 SimpleLib) = StateInit;
    def __init__(self, state_init: bytes | BoC=None):
        self.state_init = state_init
        if isinstance(self.state_init, BoC):
            self.state_init = self.state_init.hex()
    
    def to_boc(self):
        outs = Fift().run(self.build_contract_address, {
                "state_init": self.state_init,
                "network_mode_flag": 0 if App.config["network"] == "mainnet" else 2,
            }, ["result boc"])
        boc = outs["result boc"]
        return BoC(boc)
    
    def human(self):
        outs = Fift().run(self.build_contract_address, {
                "state_init": self.state_init,
                "network_mode_flag": 0 if App.config["network"] == "mainnet" else 2,
            }, ["result boc", "human readable"])
        return outs["human readable"]
