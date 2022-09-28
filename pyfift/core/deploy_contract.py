from pyfift.base.fift import Fift
from pyfift.core.boc import BoC


class DeployContract:
    build_msg_external = '''
        "Asm.fif" include
        "TonUtil.fif" include
        B{%message%} B>boc constant msg_body_unsigned
        B{%state_init%} B>boc constant init_body
        B{%destination%} B>boc <s constant dest_addr
        B{%priv_key%} constant priv_key

        // <b 0 32 u, -1 32 i, 0 32 u, b> constant msg_body_unsigned

        msg_body_unsigned hashB constant msg_hash
        msg_hash priv_key ed25519_sign constant msg_signature

        <b msg_signature B, msg_body_unsigned <s s, b> constant msg_body

        <b 
        // ext_in_msg_info$10 => '10'
        // src addr_none => '00' (from nowhere)
        b{1000} s,
        dest_addr s,
        // import_fee
        0 Gram,
        1 1 u, // has init
        0 1 u, // init ref
        init_body <s s,
        0 1 u, // body not ref
        msg_body <s s,
        b>
        constant ext_msg
        
        ext_msg 2 boc+>B constant result

        "result boc:{" type result Bx. "}" type
        '''
    build_msg_internal = '''
        "Asm.fif" include
        "TonUtil.fif" include
        B{%message%} B>boc constant msg_body
        B{%state_init%} B>boc constant init_body
        B{%destination%} B>boc <s constant dest_addr

        <b 
        // int_msg_info$0 => '0'
        // disable ihr, allow bounces and is not bounced itself => '010'
        // src addr_none => '00' 
        b{001000} s,
        dest_addr s,
        %value% Gram,
        0 1 u, // currency dict
        0 Gram, // ihr_fee
        0 Gram, // fwd_fee
        0 64 u, // created_lt
        0 32 u, // created_at
        1 1 u, // has init
        1 1 u, // init ref
        init_body ref,
        0 1 u, // body not ref
        msg_body <s s,
        b>
        constant internal_msg
        
        internal_msg 2 boc+>B constant result

        "result boc:{" type result Bx. "}" type
        '''
        # int_msg_info$0 ihr_disabled:Bool bounce:Bool bounced:Bool
        # src:MsgAddressInt dest:MsgAddressInt 
        # value:CurrencyCollection ihr_fee:Grams fwd_fee:Grams
        # created_lt:uint64 created_at:uint32 = CommonMsgInfo;

        # message$_ {X:Type} info:CommonMsgInfo
        #   init:(Maybe (Either StateInit ^StateInit))
        #   body:(Either X ^X) = Message X;
    def __init__(self, message: bytes | BoC, init: bytes | BoC, destination: bytes | BoC, priv_key: bytes | BoC, value: int):
        self.message = message or BoC("B5EE9C724101010100020000004CACB9CD") # Empty Bag
        self.init = init
        self.destination = destination
        self.priv_key = priv_key
        self.value = value

        if isinstance(self.message, BoC):
            self.message = self.message.hex()
        if isinstance(self.init, BoC):
            self.init = self.init.hex()
        if isinstance(self.destination, BoC):
            self.destination = self.destination.hex()
        if isinstance(self.priv_key, BoC):
            self.priv_key = self.priv_key.hex()
    
    def to_boc(self, external=True):
        outs = Fift().run(self.build_msg_internal if not external else self.build_msg_external, {
                "message": self.message,
                "destination": self.destination,
                "state_init": self.init,
                "priv_key": self.priv_key,
                "value": self.value,
            }, ["result boc"])
        boc = outs["result boc"]
        return BoC(boc)
