from pyfift.base.fift import Fift
import secrets


class KeyPair:
    deriv_pub_key = '''
    B{%priv_key%} priv>pub 
    "public_key:{" type Bx. "}" type
    '''
    
    def __init__(self, priv_key=None) -> None:
        if priv_key:
            if len(priv_key) == 64:
                print("using existing key defined in config ...")
                self.priv_key = priv_key
            else:
                raise RuntimeError("only 32 bytes hex strings are supported as private keys")
        else:
            print("no key is provided, generating key...")
            self.priv_key = secrets.token_hex(32).upper()
            print("private key: %s" % self.priv_key)
            print("please save your private key for later access, ideally in config.json")
        self.pub_key = self._deriv_pub()
        if not priv_key:
            print("public key: %s" % self.pub_key)
    
    
    def _deriv_pub(self):
        outs = Fift().run(self.deriv_pub_key, {
                "priv_key": self.priv_key
            }, ["public_key"])
        k = outs["public_key"]
        return k

