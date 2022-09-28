from pyfift.base.fift import Fift
from pyfift.core.boc import BoC


class ContractCode:
    build_code = '''
        "Asm.fif" include
        "TonUtil.fif" include
        "%file_address%" include 2 boc+>B constant code_boc

        "result boc:{" type code_boc Bx. "}" type
        '''
    
    def __init__(self, compiled_code_path):
        self.compiled_code_path = compiled_code_path
    
    def to_boc(self):
        outs = Fift().run(self.build_code, {
                "file_address": self.compiled_code_path,
            }, ["result boc"])
        boc = outs["result boc"]
        return BoC(boc)


def code_boc(file: str):
    return ContractCode(file).to_boc()
