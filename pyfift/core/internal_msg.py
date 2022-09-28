from pyfift.base.fift import Fift
from pyfift.core.boc import BoC


class InternalMessage:
    build_src_addr = '''
    "%src%" $>smca 2drop 2constant src_addr
    <b src_addr Addr, b> <s
    '''
    build_msg = '''
        "Asm.fif" include
        "TonUtil.fif" include
        B{%message%} B>boc constant msg_body

        %build_src%
        constant src_addr_s

        "%destination%" $>smca 2drop 2constant my_addr
        <b 
        // int_msg_info$0 => '0'
        // disable ihr, allow bounces and is not bounced itself => '010'
        // src addr_none => '00' 
        b{0010} s,
        src_addr_s s,
        my_addr Addr,
        %value% Gram,
        0 1 u, // currency dict
        0 Gram, // ihr_fee
        0 Gram, // fwd_fee
        0 64 u, // created_lt
        0 32 u, // created_at
        0 1 u, // no init
        1 1 u, // body ref
        msg_body ref,
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
    def __init__(self, message: bytes | BoC, destination: str, value: int, src: str = None):
        self.message = message
        self.destination = destination
        self.src = src
        self.value = value
        if isinstance(self.message, BoC):
            self.message = self.message.hex()
    
    def to_boc(self):
        if self.src is None:
            self.src = "b{00}"
        else:
            self.src = self.build_src_addr.replace("%src%", self.src)
        outs = Fift().run(self.build_msg, {
                "message": self.message,
                "destination": self.destination,
                "build_src": self.src,
                "value": self.value,
            }, ["result boc"])
        boc = outs["result boc"]
        return BoC(boc)
