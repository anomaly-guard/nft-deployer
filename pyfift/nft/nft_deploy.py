from pyfift.base.fift import Fift
from pyfift.core.boc import BoC
from pyfift.nft.content import build_text_obj


class DeployNFTMessage:
    build_deploy_msg = '''
        "Asm.fif" include
        "TonUtil.fif" include
        "%owner_addr%" $>smca 2drop 2constant my_addr

        %snake_content% constant snake_cell
        <b snake_cell <s s, b> constant content_cell
        <b my_addr Addr, content_cell ref, b> constant msg_cell
        <b 1 32 u, 0 64 u, %index% 64 u, %amount% Gram, msg_cell ref, b> constant msg_body
        msg_body 2 boc+>B
        "result boc:{" type Bx. "}" type
        '''
    
    def __init__(self, index, content_url, amount, owner):
        self.content_url = content_url
        self.index = index
        self.amount = amount
        self.owner = owner
    
    def to_boc(self):
        outs = Fift().run(self.build_deploy_msg, {
                "amount": self.amount,
                "owner_addr": self.owner,
                "index": self.index,
                "snake_content": build_text_obj(self.content_url).encode(),
            }, ["result boc"])
        boc = outs["result boc"]
        return BoC(boc)
