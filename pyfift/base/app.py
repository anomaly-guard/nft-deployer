import json

from pyfift.base.fift import Fift
from pyfift.base.lite_client import LiteClient
from pyfift.base.keypair import KeyPair


class App:
    fift: Fift
    lite_client: LiteClient
    key: KeyPair

    @classmethod
    def init(cls, config="config.json"):
        cls.config = json.loads(open(config).read())
        # Load Fift
        libs = cls.config["fift"]["libs"]
        cls.fift = Fift(libs)
        # Load lite_client
        l_config = cls.config["lite-client"]["config"][cls.config["network"]]
        cls.lite_client = LiteClient(l_config)
        # Load Keys
        hex_key = cls.config["private_key"]["hex"]
        cls.key = KeyPair(hex_key)
