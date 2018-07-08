from ..child.Block import Block
from ..child.Transaction import Transaction
import binascii
import sha3
from py_ecc.secp256k1 import ecdsa_raw_recover

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

    def deposit(self, value, sender): # value == msg.value on blockchain, sender = msg.sender
        new_utxo_id = len(self.utxo)
        self.utxo.append((value, sender))

        self.mintBlock(new_utxo_id, value)

        return (len(self.blockchain) - 1, new_utxo_id)

    def mintBlock(self, utxo_id, value):
        tx1 = Transaction([len(self.blockchain)], [0], [utxo_id], binascii.unhexlify("4cbc93e5a8e9e8c8f2f26689727fd164c728ee90"), value)
        block = Block([tx1])
        self.blockchain.append(block)

    def getBlock(self, blockNumber):
        return self.blockchain[blockNumber]

    # aux_sender would be the msg.sender
    def startExit(self, plasmaBlockNum, utxo, serialized_tx, proof, confirmSig, amount, aux_sender):
        if (self.utxo[utxo][1] == aux_sender):
            if (amount <= self.utxo[utxo][0]):
                self.utxo[utxo] = (self.utxo[utxo][0] - amount, self.utxo[utxo][1])
                return;

        rootMerkleTree = self.blockchain[plasmaBlockNum]
        if (amount > self.utxo[utxo][0]):
            raise Exception("You want to retire more than the UTXO you are referencing.")

        assert ecdsa_raw_recover(serialized_tx, confirmSig) == self.utxo[utxo][1]

        txHash = sha3.keccak_256(serialized_tx).hexdigest()
        assert self.attestInclusion(txHash, proof, rootMerkleTree)

    def attestInclusion(self, tx, proof, root):
        hash = tx
        for i in range(0, len(proof)):
            hash = sha3.keccak_256(self.joinHexHashes(hash,proof[i])).hexdigest()

        return hash == root;

    def joinHexHashes(self, hash1, hash2):
        union_hash = hash1 + hash2
        return binascii.unhexlify(union_hash)
