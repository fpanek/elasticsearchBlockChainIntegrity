pragma solidity ^0.8.0;

contract SimpleKeyValueStorage {
    mapping(string => string) public store;

    function set(string memory key, string memory value) public {
        store[key] = value;
    }

    function get(string memory key) public view returns (string memory) {
        return store[key];
    }
}
