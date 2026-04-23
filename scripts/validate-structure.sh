#!/bin/bash

echo "=== Reputation Kernel Monorepo Validation ==="
echo

# Check if we're in the right directory
if [ ! -f "pnpm-workspace.yaml" ]; then
    echo "❌ Not in monorepo root (pnpm-workspace.yaml not found)"
    exit 1
fi

echo "✅ Found pnpm workspace configuration"

# Check required directories
required_dirs=(
    "packages/contracts"
    "packages/ts"
    "packages/gateway"
    "packages/merkle"
    "ops"
)

for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ Directory exists: $dir"
    else
        echo "❌ Missing directory: $dir"
    fi
done

# Check required files
required_files=(
    "packages/contracts/foundry.toml"
    "packages/contracts/src/Config.sol"
    "packages/contracts/src/ReputationRegistry.sol"
    "packages/contracts/src/RootNotary.sol"
    "packages/contracts/script/DeployLocal.s.sol"
    "packages/ts/hardhat.config.ts"
    "packages/ts/package.json"
    "packages/gateway/src/index.ts"
    "packages/gateway/wrangler.toml"
    "packages/merkle/src/index.ts"
    "ops/docker-compose.yml"
    ".env.example"
    "README.md"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ File exists: $file"
    else
        echo "❌ Missing file: $file"
    fi
done

echo
echo "=== Package Structure Validation ==="

# Check package.json files
for package_dir in packages/*/; do
    if [ -f "${package_dir}package.json" ]; then
        package_name=$(basename "$package_dir")
        echo "✅ Package: $package_name has package.json"
        
        # Check if package has a name field
        if grep -q '"name"' "${package_dir}package.json"; then
            name=$(grep '"name"' "${package_dir}package.json" | head -1 | cut -d'"' -f4)
            echo "   📦 Name: $name"
        fi
    else
        echo "❌ Package: $(basename "$package_dir") missing package.json"
    fi
done

echo
echo "=== Quick Start Commands Check ==="

# Check if scripts exist in root package.json
commands=(
    "fork:base"
    "fork:eth"
    "deploy:local"
    "seed:demo"
    "gateway:dev"
    "test:ens"
)

for cmd in "${commands[@]}"; do
    if grep -q "\"$cmd\"" package.json; then
        echo "✅ Command available: pnpm $cmd"
    else
        echo "❌ Missing command: pnpm $cmd"
    fi
done

echo
echo "=== Validation Complete ==="