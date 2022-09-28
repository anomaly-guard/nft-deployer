import base64


class BoC:
    def __init__(self, data, format="hex") -> None:
        self.data = data
        self.foramt = format

    def b64(self):
        return base64.b64encode(self.bytes())

    def hex(self):
        return self.data

    def bytes(self):
        boc_bytes = bytes.fromhex(self.data)
        return boc_bytes

    def write(self, out):
        with open(out, "wb") as f:
            f.write(self.bytes())