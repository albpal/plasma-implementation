from ..child.Block import Block
from ..child.Transaction import Transaction
import binascii

class rootSCSimulator:
    blockchain = None
    utxo = None
    def __init__(self):
        self.blockchain = []
        self.utxo = []
        return;

    def submitBlock(self, root):
        char_per_byte = 2
        if len(root) != 32*char_per_byte:
            raise Exception("Merkle root length is not correct("+str(len(root))+"). Expected 32 bytes long.")
        self.blockchain.append(root)

    def deposit(self, value): # value == msg.value on blockchain
        new_utxo_id = len(self.utxo)
        self.utxo.append(value)

        self.mintBlock(new_utxo_id, value)

        return (len(self.blockchain),new_utxo_id)

    def mintBlock(self, utxo_id, value):
        tx1 = Transaction([len(self.blockchain)], [0], [utxo_id], binascii.unhexlify("4cbc93e5a8e9e8c8f2f26689727fd164c728ee90"), value)
        block = Block([tx1])
        self.blockchain.append(block)

    def startExit(plasmaBlockNum, txindex, oindex, tx, proof, confirmSig):
        return ;
