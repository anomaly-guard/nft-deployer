from pyfift.core.boc import BoC
from pyfift.base.app import App
from pyfift.core.internal_msg import InternalMessage


class WalletBase:
    def seq_no(self) -> int:
        pass

    def build_message(self, sub_wallet: int, valid_until: int, seq_no: int, message: bytes | BoC):
        pass

    def transact(self, sub_wallet: int, valid_until: int, seq_no: int, message: bytes | BoC, message_mode: int = 64):
        msg, params = self.build_message(sub_wallet, valid_until, seq_no, message, message_mode=message_mode)
        outs = App.fift.run(msg, params, ["result boc"])
        boc = outs["result boc"]
        return BoC(boc)

    def send_to_contract(self, msg_body: BoC | bytes, value: int, dst: str, sub_wallet=0, valid_until=-1, mode=64):
        m = InternalMessage(msg_body, dst, value).to_boc()
        seq_no = self.seq_no()
        msg = self.transact(sub_wallet, valid_until, seq_no, m, mode)
        s = App.lite_client.send_boc(msg)
        if s:
            print("Message successfully sent to lite-servers!")