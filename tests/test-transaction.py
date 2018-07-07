import os
import sys
current_path = os.path.dirname(__file__)
if current_path == "":
        current_path = "."
sys.path.append(current_path + '/../')
from plasma.child.Transaction import Transaction
import binascii
from py_ecc.secp256k1 import privtopub, ecdsa_raw_sign
import sha3

priv = binascii.unhexlify("c0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0de")
pub = privtopub(priv)

tx = Transaction([1,5], [20, 3], [1,1], binascii.unhexlify("fe001e973e1cfce58e4c9ef073ca10a7dbbbaa74"), 1)
unsigned_tx = tx.serialize()
print("Encoded unsigned tx: ", unsigned_tx)
v,r,s = ecdsa_raw_sign(unsigned_tx, priv)
print("Signature:",v,",",r,",",s)
tx.sign(v, r, s)
assert tx.who_signed() == pub
print("Recovered signature successfully")
assert tx.getHash() == sha3.keccak_256(unsigned_tx).hexdigest()
print("Transaction hash:", "0x" + tx.getHash())
