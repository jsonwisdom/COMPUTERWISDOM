// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {ERC20Capped} from "@openzeppelin/contracts/token/ERC20/extensions/ERC20Capped.sol";

/// @title JAYWISDOM Velocity ARCS Token
/// @notice Capped service-reward token minted only by the paired ClarityEngine.
contract JWIS is ERC20, ERC20Capped {
    uint256 public constant MAX_SUPPLY = 10_000_000 ether;

    address public immutable minter;

    error InvalidMinter();
    error NotMinter();

    constructor(address minter_) ERC20("JAYWISDOM Velocity ARCS", "JWIS") ERC20Capped(MAX_SUPPLY) {
        if (minter_ == address(0)) revert InvalidMinter();
        minter = minter_;
    }

    function mint(address to, uint256 amount) external {
        if (msg.sender != minter) revert NotMinter();
        _mint(to, amount);
    }

    function _update(address from, address to, uint256 value) internal override(ERC20, ERC20Capped) {
        super._update(from, to, value);
    }
}
