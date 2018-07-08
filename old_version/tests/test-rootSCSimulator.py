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

def test_withdrawDirectlyFromDeposit():
    priv = binascii.unhexlify("c0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0de")
    pub = privtopub(priv)

    sc = rootSCSimulator()
    (block_number, utxo)= sc.deposit(100, pub)

    sc.startExit(block_number, utxo, None, None, None, 1, pub)

def buildScenario1():
    alice_priv = binascii.unhexlify("a0dea0dea0dea0dea0dea0dea0dea0dea0dea0dea0dea0dea0dea0dea0dea0de")
    alice = privtopub(alice_priv)
    bob_priv = binascii.unhexlify("b0deb0deb0deb0deb0deb0deb0deb0deb0deb0deb0deb0deb0deb0deb0deb0de")
    bob = privtopub(bob_priv)
    carl_priv = binascii.unhexlify("c0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0dec0de")
    carl = privtopub(carl_priv)
    david_priv = binascii.unhexlify("d0ded0ded0ded0ded0ded0ded0ded0ded0ded0ded0ded0ded0ded0ded0ded0de")
    david = privtopub(david_priv)

    sc = rootSCSimulator()

    # Alice makes a deposit of 100 ETH
    (block_number, utxo)= sc.deposit(100, alice)

    # Alice makes a transaction to Bob of 5 ETH on plasma network
    tx1 = Transaction([block_number], [0], [utxo], bob, 1)
    v,r,s = ecdsa_raw_sign(tx1.serialize(), alice_priv)
    tx1.sign(v,r,s)
    # Alice makes a transaction to Carl of 5 ETH on plasma network
    tx2 = Transaction([block_number], [0], [utxo], carl, 1)
    v,r,s = ecdsa_raw_sign(tx2.serialize(), alice_priv)
    tx2.sign(v,r,s)
    # Alice makes a transaction to David of 5 ETH on plasma network
    tx3 = Transaction([block_number], [0], [utxo], david, 1)
    v,r,s = ecdsa_raw_sign(tx3.serialize(), alice_priv)
    tx3.sign(v,r,s)

    # Plasma chain build a block with the transaction performed
    block = Block([tx1, tx2, tx3])

    # Get the merkleTree of the previous block to commit it to root chain
    root = block.getMerkleTree()[0]
    # Plasma chain submit root to root chain
    sc.submitBlock(root)

    return (sc, block, tx1)

def test_withdrawFromPlasmaTX():
    (sc, block, bob_tx) = buildScenario1()   # Alice = 85 ETH, Bob = 5 ETH, Carl = 5 ETH, David = 5 ETH

    # Bob wants to withdraw the 5 ETH Alice gave him on Plasma chain but from root chain. He needs to know:
        # The blocknumber where the tx attesting Alice sent him 5TH
        # The tx (RLP_encoded) itself to attest the movement
        # The UTX0 from which Alice give him her Ethers
        # Merklee proof of the inclusion of t he TX
        # Signature attesting Alice signed the TX
    proof = block.getProof(bob_tx.getHash())
    unsigned_tx = bob_tx.serialize()
    alice_priv = binascii.unhexlify("a0dea0dea0dea0dea0dea0dea0dea0dea0dea0dea0dea0dea0dea0dea0dea0de")
    bob_priv = binascii.unhexlify("b0deb0deb0deb0deb0deb0deb0deb0deb0deb0deb0deb0deb0deb0deb0deb0de")
    bob = privtopub(bob_priv)
    v,r,s = ecdsa_raw_sign(unsigned_tx, alice_priv)
    sc.startExit(1, 0, bob_tx.serialize(), proof, (v,r,s), 5, bob)

test_withdrawDirectlyFromDeposit()
print("The user created the UTXO so it is able to withdraw (except if someone later confirm a payment)")

test_withdrawFromPlasmaTX()
print("Bob was able to withdraw 5 ETH from root chain attesting Alice sent him 5ETH on Plasma chain")
