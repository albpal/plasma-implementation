var rootChain = artifacts.require("./rootChain.sol");

contract('rootChain', function(accounts) {
  var owner_account = accounts[0];
  it("Block submit", function() {
    var rc;
    return rootChain.deployed().then(function(instance) {
      rc = instance;
      rootBlock = "0x8e61fce813b2909e7e4b534e0b77ad99c56e6b411b28559f6a3ce4065a50cc7d"
      return rc.submitBlock(rootBlock)
    }).then(function() {
       return rc.getChildChain(0);
    }).then(function(last_block)
    {
       assert.equal(last_block[0], "0x8e61fce813b2909e7e4b534e0b77ad99c56e6b411b28559f6a3ce4065a50cc7d");
    });
  });
  it("Deposit", function() {
    var rc;
    return rootChain.deployed().then(function(instance) {
      rc = instance;
      return rc.deposit({value:1})
    }).then(function() {
       assert.equal(true, true)
    });
  });
});
