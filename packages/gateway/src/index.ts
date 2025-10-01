/**
 * CCIP-Read Gateway for Reputation Kernel
 * Handles off-chain data resolution for ENS names and reputation queries
 */

interface Env {
  ETHEREUM_RPC_URL: string;
  BASE_RPC_URL: string;
  REPUTATION_REGISTRY_ADDRESS: string;
  ROOT_NOTARY_ADDRESS: string;
}

interface ReputationResponse {
  merkleRoot: string;
  timestamp: number;
  ipfsHash: string;
  notary: string;
  proof?: string;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    
    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };
    
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }
    
    try {
      // Handle CCIP-Read requests
      if (url.pathname.startsWith('/ccip-read/')) {
        const ensName = url.pathname.split('/')[2];
        return handleCCIPRead(ensName, url.searchParams, env);
      }
      
      // Handle reputation queries
      if (url.pathname.startsWith('/reputation/')) {
        const address = url.pathname.split('/')[2];
        return handleReputationQuery(address, env);
      }
      
      // Handle attestation queries
      if (url.pathname.startsWith('/attestation/')) {
        const attestationId = url.pathname.split('/')[2];
        return handleAttestationQuery(attestationId, env);
      }
      
      // Health check
      if (url.pathname === '/health') {
        return new Response(JSON.stringify({ status: 'ok', timestamp: Date.now() }), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }
      
      return new Response('Not Found', { status: 404, headers: corsHeaders });
      
    } catch (error) {
      console.error('Gateway error:', error);
      return new Response(JSON.stringify({ error: 'Internal Server Error' }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }
  },
};

async function handleCCIPRead(ensName: string, params: URLSearchParams, env: Env): Promise<Response> {
  const sender = params.get('sender');
  const data = params.get('data');
  
  if (!sender || !data) {
    return new Response(JSON.stringify({ error: 'Missing required parameters' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  // Simulate reputation data resolution
  // In a real implementation, this would query the contracts and IPFS
  const reputationData: ReputationResponse = {
    merkleRoot: '0x' + Array(64).fill('0').join(''),
    timestamp: Math.floor(Date.now() / 1000),
    ipfsHash: `Qm${ensName}ReputationData`,
    notary: '0x0000000000000000000000000000000000000000',
    proof: '0x' + Array(64).fill('1').join('')
  };
  
  // Encode response according to CCIP-Read specification
  const response = {
    data: encodeReputationData(reputationData)
  };
  
  return new Response(JSON.stringify(response), {
    headers: { 
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    }
  });
}

async function handleReputationQuery(address: string, env: Env): Promise<Response> {
  // Simulate querying reputation score and data
  const reputationScore = Math.floor(Math.random() * 1000);
  
  const response = {
    address,
    score: reputationScore,
    attestations: [],
    lastUpdated: new Date().toISOString()
  };
  
  return new Response(JSON.stringify(response), {
    headers: { 
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    }
  });
}

async function handleAttestationQuery(attestationId: string, env: Env): Promise<Response> {
  // Simulate attestation lookup
  const attestation = {
    id: attestationId,
    attester: '0x0000000000000000000000000000000000000000',
    subject: '0x0000000000000000000000000000000000000000',
    schema: 'github-contribution',
    data: 'Contributed to reputation-kernel project',
    timestamp: Math.floor(Date.now() / 1000),
    revoked: false
  };
  
  return new Response(JSON.stringify(attestation), {
    headers: { 
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    }
  });
}

function encodeReputationData(data: ReputationResponse): string {
  // Encode the response data for CCIP-Read
  // This would use ethers.js ABI encoding in a real implementation
  return '0x' + Buffer.from(JSON.stringify(data)).toString('hex');
}