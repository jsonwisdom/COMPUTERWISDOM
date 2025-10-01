# Reputation Kernel

A full-stack monorepo for a reputation kernel project, including Ethereum contracts, Hardhat tasks, a CCIP-Read gateway, and Docker Compose configurations.

## Quick Start

```bash
# Install dependencies
pnpm i

# Start local blockchain forks
pnpm fork:base   # localhost:8545 (fork Base)
pnpm fork:eth    # localhost:9545 (fork ETH)

# Deploy contracts locally
pnpm deploy:local

# Seed with demo data
pnpm seed:demo

# Start the CCIP-Read gateway
pnpm gateway:dev # localhost:3000

# Test ENS integration
pnpm test:ens
```

## Architecture

### Packages

- **`packages/contracts/`** - Solidity contracts using Foundry
  - `Config.sol` - Central configuration contract
  - `ReputationRegistry.sol` - Reputation data and attestations
  - `RootNotary.sol` - Cross-chain reputation verification
  
- **`packages/ts/`** - TypeScript SDK and Hardhat tasks
  - Deployment scripts
  - Testing utilities
  - TypeScript SDK for contract interaction
  
- **`packages/gateway/`** - Cloudflare Worker for CCIP-Read
  - Off-chain data resolution
  - ENS integration support
  - Cross-chain attestation gateway
  
- **`packages/merkle/`** - Merkle tree utilities
  - Reputation data merkle trees
  - Proof generation and verification

### Operations

- **`ops/docker-compose.yml`** - Local development environment
  - Base network fork (port 8545)
  - Ethereum network fork (port 9545)
  - IPFS node for distributed storage
  - Gateway service

## Development

### Prerequisites

- Node.js 18+
- pnpm 8+
- Docker and Docker Compose

### Environment Setup

1. Copy `.env.example` to `.env` and configure variables
2. Run the complete development setup:

```bash
pnpm setup:dev
```

This will:
- Install all dependencies
- Start blockchain forks
- Deploy contracts
- Seed demo data
- Start the gateway

### Testing

```bash
# Test all packages
pnpm test

# Test specific components
pnpm contracts:test    # Forge tests
pnpm --filter @reputation-kernel/ts test  # Hardhat tests
```

### Contract Development

```bash
# Compile contracts
pnpm contracts:compile

# Deploy to local network
pnpm contracts:deploy

# Run Forge tests
pnpm contracts:test
```

## Features

### Core Contracts

- **Reputation Registry**: Manages reputation data, attestations, and scores
- **Root Notary**: Handles cross-chain verification and proofs
- **Config**: Central configuration management

### CCIP-Read Gateway

- Off-chain data resolution for ENS names
- Reputation data aggregation
- Cross-chain attestation bridging
- IPFS integration for detailed data storage

### TypeScript SDK

- Easy contract interaction
- Reputation data queries
- Attestation creation and verification
- ENS resolution simulation

## Deployment

### Local Development

The provided Docker Compose setup creates isolated blockchain forks for development:

- Base fork: `http://localhost:8545` (Chain ID: 8453)
- Ethereum fork: `http://localhost:9545` (Chain ID: 1)

### Production

For production deployment, configure environment variables and deploy to your target networks:

```bash
# Deploy to Base mainnet
PRIVATE_KEY=your_key BASE_RPC_URL=https://mainnet.base.org pnpm deploy:local --network base

# Deploy gateway to Cloudflare Workers
cd packages/gateway && pnpm deploy
```

## License

MIT

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Original Project**: Computer Wisdom: Sovereign OS Broadcast Hub  
**Author**: Jason Wisdom (Zero Cool)  
**Transformed**: Reputation Kernel Monorepo