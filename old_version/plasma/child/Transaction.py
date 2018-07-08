import rlp
import sha3
from py_ecc.secp256k1 import ecdsa_raw_recover

class Transaction:
    blocknums = None
    tx_indexes = None
    out_indexes = None
    new_owner = None
    value = None
    (v,r,s) = (None, None, None)

    def __init__(self, blocknums, tx_indexes, out_indexes, new_owner, value):
        self.blocknums = blocknums
        self.tx_indexes = tx_indexes
        self.out_indexes = out_indexes
        self.new_owner = new_owner
        self.value = value

    def is_signed(self):
        return (v,r,s) != (None, None, None);

    def serialize(self):
        return rlp.encode([self.blocknums, self.tx_indexes, self.out_indexes, self.new_owner, self.value])

    def sign(self, v, r, s):
        (self.v, self.r, self.s) = (v,r,s)

    def who_signed(self):
        return ecdsa_raw_recover(self.serialize(), (self.v, self.r, self.s))

    def getHash(self):
        return sha3.keccak_256(self.serialize()).hexdigest()
