pragma solidity ^0.4.23;

contract rootChain {
    address public operator;
    uint256 public currentChildBlock;
    mapping (uint256 => ChildBlock) public childChain;


    event BlockSubmitted(
        bytes32 root,
        uint256 timestamp
    );

    struct ChildBlock {
        bytes32 root;
        uint256 timestamp;
    }

    event Deposit(
        address indexed depositor,
        uint256 indexed depositBlock,
        address token,
        uint256 amount
    );
    modifier onlyOperator() {
        require(msg.sender == operator);
        _;
    }

    constructor()
       public
    {
        operator = msg.sender;
        currentChildBlock = 0;
    }

    function submitBlock(bytes32 _root)
       public
       onlyOperator
    {
        childChain[currentChildBlock] = ChildBlock({
            root: _root,
            timestamp: block.timestamp
        });

       // Update block numbers.
        currentChildBlock = currentChildBlock + 1;

        emit BlockSubmitted(_root, block.timestamp);
    }

    function getChildChain(uint256 _blockNumber)
        public
        view
        returns (bytes32, uint256)
    {
        return (childChain[_blockNumber].root, childChain[_blockNumber].timestamp);
    }

    // TODO
    function deposit()
        public
        payable
    {
        // Only allow up to CHILD_BLOCK_INTERVAL deposits per child block.
        //require(currentDepositBlock < CHILD_BLOCK_INTERVAL);

        bytes32 root = keccak256(msg.sender, address(0), msg.value);
 
        uint depositBlock = currentChildBlock + 1;
        childChain[depositBlock] = ChildBlock({
            root: root,
            timestamp: block.timestamp
        });
        currentChildBlock = depositBlock;

        emit Deposit(msg.sender, depositBlock, address(0), msg.value);
    }
}
