import os
import sys
import binascii
current_path = os.path.dirname(__file__)
if current_path == "":
        current_path = "."
sys.path.append(current_path + '/..')
from plasma.rootchain.rootSCSimulator import rootSCSimulator
from plasma.child.Transaction import Transaction
from plasma.child.Block import Block

from py_ecc.secp256k1 import privtopub, ecdsa_raw_sign

priv = binascii.unhexlify("c0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0de")
pub = privtopub(priv)

tx1 = Transaction([1,5], [20, 3], [1,1], binascii.unhexlify("fe001e973e1cfce58e4c9ef073ca10a7dbbbaa74"), 1)
tx2 = Transaction([2,6], [1, 5], [1,1], binascii.unhexlify("fe002e973e1cfce58e4c9ef073ca10a7dbbbaa74"), 1)
tx3 = Transaction([3,7], [14, 8], [1,2], binascii.unhexlify("fe003e973e1cfce58e4c9ef073ca10a7dbbbaa74"), 1)
tx4 = Transaction([4,8], [3, 6], [2,1], binascii.unhexlify("fe004e973e1cfce58e4c9ef073ca10a7dbbbaa74"), 1)

for tx in [tx1, tx2, tx3, tx4]:
    unsigned_tx = tx.serialize()
    v,r,s = ecdsa_raw_sign(unsigned_tx, priv)
    tx.sign(v, r, s)

block = Block([tx1, tx2, tx3, tx4])

merkleTree = block.getMerkleTree()

sc = rootSCSimulator()

sc.submitBlock(merkleTree[0])
print("Block submitted.")

(block_number, txindex, utxo, txraw)= sc.deposit(5)
print("Deposit done. Asigned block: " + str(block_number) + ", assigned UTXO: ", str(utxo))

# Let's exit from plasma sidechain
#    def startExit(plasmaBlockNum, txindex, oindex, tx, proof, confirmSig):
sc.startExit(block_number, )
