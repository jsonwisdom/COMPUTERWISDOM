#!/bin/bash

# Install Foundry dependencies for the reputation kernel project

echo "Installing Foundry dependencies..."

cd packages/contracts

# Initialize forge if not already done
if [ ! -f "foundry.toml" ]; then
    forge init --no-git --force .
fi

# Install OpenZeppelin contracts
forge install OpenZeppelin/openzeppelin-contracts --no-commit

# Install Forge Standard Library
forge install foundry-rs/forge-std --no-commit

# Update remappings
echo "forge-std/=lib/forge-std/src/" > remappings.txt
echo "openzeppelin-contracts/=lib/openzeppelin-contracts/" >> remappings.txt
echo "@openzeppelin/=lib/openzeppelin-contracts/" >> remappings.txt

echo "Foundry dependencies installed successfully!"

# Build contracts to verify installation
echo "Building contracts..."
forge build

echo "Setup complete!"