#!/bin/bash

# Demo script showing the reputation kernel monorepo in action

echo "🚀 Reputation Kernel Monorepo Demo"
echo "=================================="
echo

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check if pnpm is available
if ! command -v pnpm &> /dev/null; then
    echo "❌ pnpm is not installed"
    echo "   Install with: curl -fsSL https://get.pnpm.io/install.sh | sh"
    exit 1
fi
echo "✅ pnpm found: $(pnpm --version)"

# Check if docker is available
if ! command -v docker &> /dev/null; then
    echo "⚠️  Docker not found - Docker commands will not work"
else
    echo "✅ Docker found: $(docker --version | head -1)"
fi

echo

# Validate structure
echo "🔍 Validating monorepo structure..."
./scripts/validate-structure.sh | grep -E "✅|❌" | tail -20
echo

echo "📚 Available Commands:"
echo "====================="

echo "🔧 Development Setup:"
echo "  pnpm i              # Install all dependencies"
echo "  pnpm fork:base       # Start Base network fork (localhost:8545)"
echo "  pnpm fork:eth        # Start Ethereum network fork (localhost:9545)"
echo "  pnpm setup:dev       # Complete development setup"
echo

echo "📦 Contract Development:"
echo "  pnpm contracts:compile  # Compile Solidity contracts"
echo "  pnpm contracts:test     # Run Forge tests"
echo "  pnpm deploy:local       # Deploy contracts locally"
echo

echo "🌐 Gateway & SDK:"
echo "  pnpm gateway:dev        # Start CCIP-Read gateway (localhost:3000)"
echo "  pnpm seed:demo          # Populate with demo data"
echo "  pnpm test:ens           # Test ENS integration"
echo

echo "🏗️ Build & Test:"
echo "  pnpm build              # Build all packages"
echo "  pnpm test               # Run all tests"
echo

echo "📁 Project Structure:"
echo "===================="
echo "packages/"
echo "├── contracts/      # Foundry + Solidity contracts"
echo "│   ├── src/        # Config.sol, ReputationRegistry.sol, RootNotary.sol"
echo "│   ├── script/     # DeployLocal.s.sol"
echo "│   └── test/       # Forge tests"
echo "├── ts/             # TypeScript SDK + Hardhat"
echo "│   ├── src/        # ReputationKernelSDK"
echo "│   └── scripts/    # deploy.ts, seed.ts, test-ens.ts"
echo "├── gateway/        # Cloudflare Worker for CCIP-Read"
echo "│   └── src/        # Gateway implementation"
echo "└── merkle/         # Merkle tree utilities"
echo "    └── src/        # ReputationMerkleTree"
echo
echo "ops/"
echo "└── docker-compose.yml  # Local blockchain forks + IPFS"
echo

echo "💡 Quick Start Example:"
echo "======================"
echo "# 1. Install dependencies"
echo "pnpm i"
echo
echo "# 2. Start local blockchain forks"
echo "pnpm fork:base &    # Base fork on port 8545"
echo "pnpm fork:eth &     # Ethereum fork on port 9545"
echo
echo "# 3. Deploy contracts"
echo "export PRIVATE_KEY=0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
echo "pnpm deploy:local"
echo
echo "# 4. Seed with demo data"
echo "pnpm seed:demo"
echo
echo "# 5. Start the gateway"
echo "pnpm gateway:dev &  # Gateway on port 3000"
echo
echo "# 6. Test ENS integration"
echo "pnpm test:ens"
echo

echo "🌟 Key Features:"
echo "==============="
echo "✅ Cross-chain reputation verification"
echo "✅ Merkle tree proofs for reputation data"
echo "✅ Attestation system for reputation claims"
echo "✅ CCIP-Read gateway for ENS integration"
echo "✅ TypeScript SDK for easy integration"
echo "✅ Local development environment with Docker"
echo "✅ Comprehensive testing and validation"
echo

echo "📖 For more information, see README.md"
echo

# Check if any development servers are running
echo "🔍 Checking for running services..."
if lsof -i :8545 &> /dev/null; then
    echo "✅ Base fork running on port 8545"
else
    echo "⭕ Base fork not running (use: pnpm fork:base)"
fi

if lsof -i :9545 &> /dev/null; then
    echo "✅ Ethereum fork running on port 9545"
else
    echo "⭕ Ethereum fork not running (use: pnpm fork:eth)"
fi

if lsof -i :3000 &> /dev/null; then
    echo "✅ Gateway running on port 3000"
else
    echo "⭕ Gateway not running (use: pnpm gateway:dev)"
fi

echo
echo "🎉 Demo complete! The reputation kernel monorepo is ready for development."