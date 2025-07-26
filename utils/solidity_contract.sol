pragma solidity ^0.8.0;

contract FederatedLearning {
    uint public learningRate;
    uint public batchSize;
    uint public epochs;

    constructor(uint _learningRate, uint _batchSize, uint _epochs) {
        learningRate = _learningRate;
        batchSize = _batchSize;
        epochs = _epochs;
    }

    function updateParameters(uint _learningRate, uint _batchSize, uint _epochs) public {
        learningRate = _learningRate;
        batchSize = _batchSize;
        epochs = _epochs;
    }
}
