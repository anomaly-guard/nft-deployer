from pyfift.base.app import App
from pyfift.core.contract import Contract
from pyfift.core.boc import BoC
from pyfift.wallet.wallet_base import WalletBase


class WalletV3R2(Contract, WalletBase):
    code = "B5EE9C724101010100710000DEFF0020DD2082014C97BA218201339CBAB19F71B0ED44D0D31FD31F31D70BFFE304E0A4F2608308D71820D31FD31FD31FF82313BBF263ED44D0D31FD31FD3FFD15132BAF2A15144BAF2A204F901541055F910F2A3F8009320D74A96D307D402FB00E8D101A4C8CB1FCB1FCBFFC9ED5410BD6DAD"
    initial_dep_msg = '''
    "Asm.fif" include
    "TonUtil.fif" include

    <b 0 32 u, -1 32 i, 0 32 u, b> 2 boc+>B constant msg
    "result boc:{" type msg Bx. "}" type
    '''
    state_init = '''
    "Asm.fif" include
    "TonUtil.fif" include
    B{%pub_key%} 256 B>u@ constant pub_key
    
    <b 
    0 32 u, // seq-no
    0 32 u, // subwallet
    pub_key 256 u,
    b>
    constant addr_f
    addr_f 2 boc+>B constant result
    "result boc:{" type result Bx. "}" type
    '''
    build_msg = '''
        "Asm.fif" include
        "TonUtil.fif" include
        B{%message%} B>boc
        constant message_bd

        B{%priv_key%} constant priv_key
        "%wallet_addr%" $>smca 2drop 2constant my_addr

        <b %sub_wallet% 32 u, %valid_until% 32 %v_ui%, %seq_no% 32 u, %message_mode% 8 u, message_bd ref, b> constant msg_body_unsigned

        msg_body_unsigned hashB constant msg_hash
        msg_hash priv_key ed25519_sign constant msg_signature

        <b msg_signature B, msg_body_unsigned <s s, b> constant msg_body

       <b 
        // ext_in_msg_info$10 => '10'
        // src addr_none => '00' (from nowhere)
        b{1000} s,
        my_addr Addr,
        // import_fee
        0 Gram,
        // Now we go through message body:
        // no init field => '0'
        // body as ref => '1'
        b{01} s, 
        msg_body ref,
        b>
        constant external_msg
        
        external_msg 2 boc+>B constant result

        "result boc:{" type result Bx. "}" type
        '''

    def __init__(self):
        self.init_code(code_hex=WalletV3R2.code)

    def pub_key(self) -> int:
        o = App.lite_client.get_method(78748, self.address(binary=False))
        return int(o.strip())

    def seq_no(self) -> int:
        o = App.lite_client.get_method(85143, self.address(binary=False))
        return int(o.strip())
    
    def init_data(self, pub_key: bytes | BoC = None):
        pub_key = pub_key or App.key.pub_key
        pub_key = pub_key.hex() if isinstance(pub_key, BoC) else pub_key
        outs = App.fift.run(self.state_init, {
                "pub_key": pub_key,
            }, ["result boc"])
        boc = outs["result boc"]
        self.data = BoC(boc)

    def initial_msg(self):
        outs = App.fift.run(self.initial_dep_msg, {}, ["result boc"])
        boc = outs["result boc"]
        return BoC(boc)

    def build_message(self, sub_wallet: int, valid_until: int, seq_no: int, message: bytes | BoC, message_mode: int = 64):
        if isinstance(message, bytes):
            message = message.encode('hex')
        if isinstance(message, BoC):
            message = message.hex()
        return self.build_msg, {
            "message": message,
            "wallet_addr": self.address(binary=False),
            "sub_wallet": sub_wallet,
            "valid_until": valid_until,
            "v_ui": "i" if valid_until == -1 else "u",
            "seq_no": seq_no,
            "priv_key": App.key.priv_key,
            "message_mode": message_mode,
        }