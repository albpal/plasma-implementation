# Project description
This projects aims to implement the Plasma framework described at https://plasma.io with two main objectives. In order of priority:

1. Understand Plasma framework
2. Develop an implementation of Plasma framework

## Restrictions
Despite Plasma paper, we will focus on implementations where Ethereum public network is the root chain and only 1 level of depth is possible. We won't detail the kind of blockchain network built (sidechain SPV based, drive chain, etc.). We will simply refer to l1 (level 1 or root chain), l2 (blockchain committing to lv1), etc.

## Main concerns
### How is value sent to l2 chain?
We defined *rootContract* as the contract deployed on the Ethereum blockchain.
I have 5 ETH and want to transfer 1 of them to this l2 chain. I sent 1 ETH to *rootContract* attached on a transaction executing *deposit()* function.

### How value is transferred in l2 and correctly reflected on l1?
### How is value sent back to root chain?
### How users can be sure funds locked on root chain are not stolen?


# References:
1. https://plasma.io/plasma.pdf
2. https://ethresear.ch/t/minimal-viable-plasma
3. https://github.com/omisego/plasma-mvp
