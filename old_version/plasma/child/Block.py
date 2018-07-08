import sha3
import rlp
import binascii

class Block:
    transactions = []
    rootMerkleTree = []
    merkleTree = []
    def __init__(self, transactions):
        if len(transactions) % 2 != 0:
            transactions.append(transactions[-1])
        self.transactions = transactions
        self.merkleTree = self.getMerkleTree()
        self.rootMerkleTree = self.merkleTree[0]

    def getrootMerkleTree(self):
        return self.rootMerkleTree

    def joinHexHashes(self, hash1, hash2):
        union_hash = hash1 + hash2
        return binascii.unhexlify(union_hash)

    def generateMerkleTree(self, hashes):
        assert len(hashes) % 2 == 0

        if len(hashes) == 2:
            hashes.insert(0, sha3.keccak_256(self.joinHexHashes(hashes[0], hashes[1])).hexdigest())
            return hashes

        new_hashes = []
        for i in range(0,len(hashes),2):
            new_hashes.append(sha3.keccak_256(self.joinHexHashes(hashes[i], hashes[i+1])).hexdigest())
        return self.generateMerkleTree(new_hashes) + hashes

    def getMerkleTree(self):
        tx_hashes = []
        for tx in self.transactions:
            tx_hashes.append(tx.getHash())

        return self.generateMerkleTree(tx_hashes)

    def getProof(self, txhash):
        txposition = self.lookupTransactionPosition(txhash)
        #print("Transaction " + txhash + " fount at position ", txposition)
        return self.getProofPath(txposition, self.merkleTree, len(self.transactions))

    def lookupTransactionPosition(self, txraw):
        index = -1
        for i in range(0, len(self.merkleTree) - 1):
            if txraw == self.merkleTree[i]:
                index = i+1
                break
        if index == -1:
            raise Exception("Transaction " + str(txraw) + " not found.")
        return index

    def getProofPath(self, txposition, merkleTree, leavesnumber):
        #print("TX position: ", txposition)
        #print("Merklee level: ", merkleTree)
        #print("leavesnumber: ", leavesnumber)
        if (leavesnumber == 1):
            return []

        if (txposition == 1 or txposition == 2):
            next_position = 0
        else:
            next_position = int(leavesnumber/2)

        #print("Step: ", step)
        if txposition % 2 == 0:
            proof = [merkleTree[txposition]]
            proof.extend(self.getProofPath(next_position, merkleTree[:-leavesnumber], int(leavesnumber/2)))
        else:
            proof = [merkleTree[txposition - 1]]
            proof.extend(self.getProofPath(next_position, merkleTree[:-leavesnumber], int(leavesnumber/2)))
        return proof

    def attestInclusion(self, tx, proof):
        hash = tx
        for i in range(0, len(proof)):
            hash = sha3.keccak_256(self.joinHexHashes(hash,proof[i])).hexdigest()
        return hash == self.rootMerkleTree;
