import rlp
from py_ecc.secp256k1 import ecdsa_raw_recover

class Transaction:
    is_signed = None
    blocknums = None
    tx_indexes = None
    out_indexes = None
    new_owner = None
    value = None
    v = None
    r = None
    s = None
    def __init__(self, blocknums, tx_indexes, out_indexes, new_owner, value):
        self.is_signed = False
        self.blocknums = blocknums
        self.tx_indexes = tx_indexes
        self.out_indexes = out_indexes
        self.new_owner = new_owner
        self.value = value

    def is_signed(self):
        return self.is_signed;

    def serialize(self):
        return rlp.encode([self.blocknums, self.tx_indexes, self.out_indexes, self.new_owner, self.value])

    def sign(self, v, r, s):
        self.is_signed = True
        self.v, self.r, self.s = v,r,s
        return ecdsa_raw_recover(self.serialize(), (v, r, s))
