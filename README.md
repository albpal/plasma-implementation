# Project description
This project aims to implement the Plasma framework described at https://plasma.io with two main objectives. In order of priority:

1. Understand Plasma framework
2. Develop an implementation of Plasma framework

## Motivation
InterLedger Protocols are one of the cornerstone pieces of the blockchain ecosystem. Public blockchains are a **trusty brand technology** but without someone behind it. How it has become a trusty platform are beyond the scope of this description.

Maybe the big ones (GAFA, etc.) have a big reputation and the majority of users rely on them. But how can a small/unknown business achieve this level of reputation and reliability? Nowadays, it can be expensive: community generation, marketing, for free products/events, legal concerns, etc. However, now they can use blockchain as a trusty platform and bring trust and reliability to the users. Blockchain is becoming a standard for trust.

Despite the aforementioned, public blockchains have its own limitations. First of all, they have a very limited transactions per second. Many businesses need a higher throughput. Second, the cost per transaction cannot be acceptable for many business either ([storage cost](https://medium.com/@albpalau/desarrollando-sobre-ethereum-tipos-de-almacenamientos-5b4bc0b63c3a)). So, how can businesses benefit from blockchain while still keeping the quality of its services?

InterLedger Protocols (ILP) try to solve the above problems. The businesses will use an alternative blockchain with the requirements they need and will _subscribe_ eventually to a public blockchain (or another trustier). The way the subscribtion is performed has to follow rules to be enough trusty so the users know that:

1. They can bring their assets to a child blockchain in a secure way
2. If the child blockchain operator is corrupted or malicious, they can exit from child blockchain without loose their funds

Plasma is a framework or guidance to implement a protocol to achieve that but there are others: Polkadot, Cosmos, Drivechains, side chains, etc.  ([bc scalability](https://medium.com/@albpalau/la-escalabilidad-en-blockchains-p%C3%BAblicas-5ba5408622c9))

## Common problems to solve
There are common problems to be solved by an ILP implementation **on the root blockchain** (the most trusted). We shall describe them:

1. Attest a transaction has happening on the child blockchain
2. Attest the ownership of a transaction included in a commit
3. Resolve disputes

If our protocol can solve them at the same time, we may use it to interact between different blockchains.

### Attest a transaction has happening on the child blockchain
As we mentioned earlier, child blockchain will _subcribe_ to the parent blockchain. The subcription can consist on commiting a [Merkle Tree](https://medium.com/@albpalau/tokenizaci%C3%B3n-%C3%A1rbol-de-merkle-1276820a1d60) root hash to the parent blockchain so we can batch the transactions happening on the child one and potentially scale to millions of transactions.

To attest a transaction has been included in one of the commits of the child blockchain, the user has to hold two pieces of information:

1. The transaction itself in a clear format (not hashed or encrypted)
2. A proof path to the root hash

Code example (Python):

```python
    def attestInclusion(self, tx, proof):
        hash = tx
        for i in range(0, len(proof)):
            hash = sha3.keccak_256(self.joinHexHashes(hash,proof[i])).hexdigest()
        return hash == self.rootMerkleTree;
```

### Attest the ownership of a transaction included in a commit
The transaction has to be something similar to:

```
[blknum1, txindex1, oindex1, sig1, # Input 1
 blknum2, txindex2, oindex2, sig2, # Input 2
 newowner1, denom1,                # Output 1
 newowner2, denom2,                # Output 2
 fee]
```
So it identifies who is the new owner of a particular amount.

If you can both attest inclusion of a transaction and ownership, you will be able to withdraw funds from the parent blockchain.

### Resolve disputes
The algorithm on the root blockchain only check for the two previous attestations when an user wants to withdraw funds. However, it doesn't check all the history of the blocks, it only stores hashes. The users (or a service) has to monitor the blockchain. Let's suppose

    A has 1 ETH in a particular block committed at date X
    A sends 1ETH to B. A new block is generated and committed at a later date Y

What happens if A wants to withdraw 1 ETH on the root blockchain he/she has at date X? The algorithm will accept both attestations. B has to detect that A wants to withdraw funds that has been already expended and he/she has to send a proof of fraud, ie, show a transaction attesting A has spend the value in a later block. In fact, this proof of fraud can be done by anyone. To allow these proof of fraud, users that want to withdraw value, have to wait a period of time before the funds are sent back to the user.

## Scope of the project
Despite Plasma paper, we will focus on implementations where Ethereum public network is the root chain and only 1 level of depth is possible. We won't detail the kind of blockchain network built (sidechain SPV based, drive chain, etc.) upon it. We will simply refer to l1 (level 1 or root chain), l2 (blockchain committing to lv1), etc.

# Setup the project
The project has been built with [Truffle](https://truffleframework.com/). Install it to fully integrate with the development pipeline.

1. Clone the project:

```
git clone https://github.com/albpal/plasma-implementation.git
cd plasma
```

2. Build the smart contracts:

```truffle compile```

3. Deploy the smart contracts to a development blockchain. [Ganache](https://truffleframework.com/ganache) is a good choice.

```truffle deploy```

4. Run the tests:

```
truffle test
Using network 'development'.



  Contract: rootChain
    ✓ Block submit (178ms)
    ✓ Deposit (128ms)


  2 passing (430ms)

```

5. Enjoy!

# References:
1. https://plasma.io/plasma.pdf
2. https://ethresear.ch/t/minimal-viable-plasma
3. https://github.com/omisego/plasma-mvp
