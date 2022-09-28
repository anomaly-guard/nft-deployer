from pyfift.nft.utils import chunker

# tail#_ {bn:#} b:(bits bn) = SnakeData ~0;
# cons#_ {bn:#} {n:#} b:(bits bn) next:^(SnakeData ~n) = SnakeData ~(n + 1);
class SnakeData:
    bits: bytes
    ref: "SnakeData"

    def __init__(self, bits=None, ref=None):
        self.bits = bits
        self.ref = ref
    
    def encode(self):
        c = "<b {bits} {next} b>"
        bits = "x{%s} s," % self.bits.hex()
        next_ = ""
        if self.ref is not None:
            t = self.ref.encode()
            next_ = "%s ref," % t
        return c.format(bits=bits, next=next_)
    
    @staticmethod
    def build(chunks):
        if len(chunks) == 0: 
            return None
        c = chunks[0]
        return SnakeData(bits=c, ref=SnakeData.build(chunks[1:]))

def build_text_obj(url):
    b = bytearray(url.encode("ascii"))
    max_cell_size = 1023 // 8
    chunks_ = list(chunker(b, max_cell_size))
    return SnakeData.build(chunks_)