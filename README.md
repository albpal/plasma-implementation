# Project description
This projects aims to implement the Plasma framework described at https://plasma.io with two main objectives. In order of priority:

1. Understand Plasma framework
2. Develop an implementation of Plasma framework

## Restrictions
Despite Plasma paper, we will focus on implementations where Ethereum public network is the root chain and only 1 level of depth is possible. We won't detail the kind of blockchain network built (sidechain SPV based, drive chain, etc.). We will simply refer to l1 (level 1 or root chain), l2 (blockchain committing to lv1), etc.

## Architecture
There are three main pieces:
* Ethereum main network
* Plasma chain network
* Plasma anchoring

### Ethereum main network
It's a smart contract deployed on Ethereum public network. It will maintain, mainly, the following data structure:
* Block list. Each one containing:
  * The root of a Merkle Tree (whatever how plasma chain bundles the transactions)
  * Block timestamp

### Plasma chain network
The child chain where transactions can reference UTXO from the main network and transact with them without committing to Ethereum. The consensus and client implementation can be arbitrary but data has to be available to the parties involved in a transaction.

# References:
1. https://plasma.io/plasma.pdf
2. https://ethresear.ch/t/minimal-viable-plasma
3. https://github.com/omisego/plasma-mvp
