from pyfift.base.app import App
from pyfift.base.fift import Fift
from pyfift.core.boc import BoC
from pyfift.core.code import code_boc
from pyfift.core.contract import Contract
from pyfift.nft.content import build_text_obj


class NftCollection(Contract):
    build_collection_storage = '''
        "Asm.fif" include
        "TonUtil.fif" include

        B{%item_code%} B>boc
        constant nft_item_code

        "%wallet_addr%" $>smca 2drop 2constant my_addr

        // Royalty Cell
        <b %royalty_factor% 16 u, %royalty_base% 16 u, my_addr Addr, b> constant royalty_cell

        // Contents
        %gen_collection_content% constant collection_content
        %gen_common_content% constant common_content

        // Content Cells
        <b 1 8 u, collection_content <s s, b> constant collection_content_c
        <b 1 8 u, common_content <s s, b> constant common_content_c
        <b collection_content_c ref, common_content ref, b> constant contents_cell

        // Storage Cell
        <b my_addr Addr, %next_item_index% 64 u, contents_cell ref, nft_item_code ref, royalty_cell ref, b>

        2 boc+>B
        "result boc:{" type Bx. "}" type
        '''
    def __init__(self) -> None:
        self.item_code = code_boc(App.config["contract-codes"]["nft"]["item"]).hex()
        self.init_code(code_path=App.config["contract-codes"]["nft"]["collection"])

    def init_data(self, owner=None, royalty_factor=0, royalty_base=1, next_item_index=0, collection_content_url='', common_content_url=''):
        self.wallet_addr = owner
        self.royalty_factor = royalty_factor
        self.royalty_base = royalty_base
        self.next_item_index = next_item_index
        self.collection_content_url = collection_content_url
        self.common_content_url = common_content_url
        self.data = self._to_boc()
    
    def _to_boc(self):
        outs = Fift().run(self.build_collection_storage, {
                "item_code": self.item_code,
                "wallet_addr": self.wallet_addr,
                "royalty_factor": self.royalty_factor,
                "royalty_base": self.royalty_base,
                "next_item_index": self.next_item_index,
                "gen_collection_content": build_text_obj(self.collection_content_url).encode(),
                "gen_common_content": build_text_obj(self.common_content_url).encode(),
            }, ["result boc"])
        boc = outs["result boc"]
        return BoC(boc)
