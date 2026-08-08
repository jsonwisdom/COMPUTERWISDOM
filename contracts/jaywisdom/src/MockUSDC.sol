// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

/// @notice Test-only six-decimal payment token. Never use as a mainnet asset.
contract MockUSDC is ERC20 {
    constructor(address recipient, uint256 amount) ERC20("Mock USD Coin", "mUSDC") {
        _mint(recipient, amount);
    }

    function decimals() public pure override returns (uint8) {
        return 6;
    }

    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }
}
