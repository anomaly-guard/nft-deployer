from pyfift.base.fift import Fift
from pyfift.core.boc import BoC


class StateInit:
    build_state_init = '''
        "Asm.fif" include
        "TonUtil.fif" include
        B{%code%} B>boc
        constant contract_code

        B{%data%} B>boc
        constant contract_data

        // State Init
        <b b{001} s, contract_code ref, 1 1 u, contract_data ref, null dict, b>
        2 boc+>B

        "result boc:{" type Bx. "}" type
        '''

    # _ split_depth:(Maybe (## 5)) special:(Maybe TickTock)
    #   code:(Maybe ^Cell) data:(Maybe ^Cell)
    #   library:(HashmapE 256 SimpleLib) = StateInit;
    def __init__(self, code: bytes | BoC=None, data: bytes | BoC=None):
        self.code = code
        self.data = data
        if isinstance(self.code, BoC):
            self.code = self.code.hex()
        if isinstance(self.data, BoC):
            self.data = self.data.hex()
    
    def to_boc(self):
        outs = Fift().run(self.build_state_init, {
                "code": self.code,
                "data": self.data,
            }, ["result boc"])
        boc = outs["result boc"]
        return BoC(boc)
