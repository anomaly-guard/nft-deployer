from pyfift.base.app import App
from pyfift.wallet._wallet_base import WalletBase
from pyfift.core.boc import BoC
from pyfift.base.fift import Fift


class WalletV3R2(WalletBase):
    code = "B5EE9C724101010100710000DEFF0020DD2082014C97BA218201339CBAB19F71B0ED44D0D31FD31F31D70BFFE304E0A4F2608308D71820D31FD31FD31FF82313BBF263ED44D0D31FD31FD3FFD15132BAF2A15144BAF2A204F901541055F910F2A3F8009320D74A96D307D402FB00E8D101A4C8CB1FCB1FCBFFC9ED5410BD6DAD"
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

        <b %sub_wallet% 32 u, %valid_until% 32 u, %seq_no% 32 u, %message_mode% 8 u, message_bd ref, b> constant msg_body_unsigned

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

    def pub_key(self) -> int:
        o = self.client.get_method(78748, self.address)
        return int(o.strip())

    def seq_no(self) -> int:
        o = self.client.get_method(85143, self.address)
        return int(o.strip())
    
    @classmethod
    def init_data(cls, pub_key: bytes | BoC = None):
        pub_key = pub_key or App.key.pub_key
        if isinstance(pub_key, BoC):
            pub_key = pub_key.hex()
        outs = App.fift.run(cls.state_init, {
                "pub_key": pub_key,
            }, ["result boc"])
        boc = outs["result boc"]
        return BoC(boc)

    def build_message(self, sub_wallet: int, valid_until: int, seq_no: int, message: bytes | BoC, message_mode: int = 64):
        if isinstance(message, bytes):
            message = message.encode('hex')
        if isinstance(message, BoC):
            message = message.hex()
        return self.build_msg, {
            "message": message,
            "wallet_addr": self.address,
            "sub_wallet": sub_wallet,
            "valid_until": valid_until,
            "seq_no": seq_no,
            "priv_key": self.priv_key,
            "message_mode": message_mode,
        }