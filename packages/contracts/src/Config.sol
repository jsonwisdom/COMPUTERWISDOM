// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Ownable} from "lib/openzeppelin-contracts/contracts/access/Ownable.sol";

/**
 * @title Config
 * @dev Central configuration contract for the reputation kernel system
 */
contract Config is Ownable {
    /// @notice Mapping of configuration keys to values
    mapping(string => bytes) public configs;
    
    /// @notice Emitted when a configuration is updated
    event ConfigUpdated(string indexed key, bytes value);
    
    constructor(address _owner) Ownable(_owner) {}
    
    /**
     * @notice Set a configuration value
     * @param key The configuration key
     * @param value The configuration value
     */
    function setConfig(string calldata key, bytes calldata value) external onlyOwner {
        configs[key] = value;
        emit ConfigUpdated(key, value);
    }
    
    /**
     * @notice Get a configuration value
     * @param key The configuration key
     * @return The configuration value
     */
    function getConfig(string calldata key) external view returns (bytes memory) {
        return configs[key];
    }
    
    /**
     * @notice Get a configuration value as address
     * @param key The configuration key
     * @return The configuration value as address
     */
    function getAddress(string calldata key) external view returns (address) {
        bytes memory value = configs[key];
        require(value.length == 20, "Config: invalid address length");
        return abi.decode(value, (address));
    }
    
    /**
     * @notice Get a configuration value as uint256
     * @param key The configuration key
     * @return The configuration value as uint256
     */
    function getUint256(string calldata key) external view returns (uint256) {
        bytes memory value = configs[key];
        return abi.decode(value, (uint256));
    }
}