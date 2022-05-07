// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.1;

contract SimpleStorage {
    struct People {
        uint256 favoriteNumber;
        string name;
    }

    // this will initialize favoriteNumber as 0!
    uint256 favoriteNumber;
    People[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;

    function store(uint256 _favoriteNumber) public returns (uint256){
        favoriteNumber = _favoriteNumber;
        return favoriteNumber;
    }

    function retrieve() public view returns(uint256) {
        return favoriteNumber;
    }

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}