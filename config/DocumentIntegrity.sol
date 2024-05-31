// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract DocumentIntegrity {
    event ChecksumAdded(string indexed index, string indexed documentId, string checksum);
    event ChecksumQueried(string indexed index, string documentId);

    mapping(string => mapping(string => string)) private checksums;
    mapping(string => string[]) private keys;

    function addChecksumEntry(string memory _index, string memory _documentId, string memory _checksum) public {
        checksums[_index][_documentId] = _checksum;
        keys[_index].push(_documentId);
        emit ChecksumAdded(_index, _documentId, _checksum);
    }

    function getChecksumEntry(string memory _index, string memory _documentId) public view returns (string memory) {
        return checksums[_index][_documentId];
    }

    function getAllChecksums(string memory _index) public view returns (string[] memory documentIds, string[] memory checksumsArray) {
        uint length = keys[_index].length;
        documentIds = new string[](length);
        checksumsArray = new string[](length);

        for (uint i = 0; i < length; ++i) {
            documentIds[i] = keys[_index][i];
            checksumsArray[i] = checksums[_index][keys[_index][i]];
        }

        return (documentIds, checksumsArray);
    }
}
