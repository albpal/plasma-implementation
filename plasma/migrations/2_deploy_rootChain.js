var rootChain = artifacts.require("./rootChain.sol");

module.exports = function(deployer) {
  deployer.deploy(rootChain);
};
