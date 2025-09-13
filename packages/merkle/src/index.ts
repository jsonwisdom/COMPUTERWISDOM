import { MerkleTree } from 'merkletreejs';
import keccak256 from 'keccak256';

export interface ReputationEntry {
  address: string;
  score: number;
  attestations: string[];
  metadata?: Record<string, any>;
}

export interface MerkleProof {
  leaf: string;
  proof: string[];
  root: string;
  index: number;
}

export class ReputationMerkleTree {
  private tree: MerkleTree;
  private leaves: string[];
  private entries: ReputationEntry[];

  constructor(entries: ReputationEntry[]) {
    this.entries = entries;
    this.leaves = entries.map(entry => this.hashEntry(entry));
    this.tree = new MerkleTree(this.leaves, keccak256, { sortPairs: true });
  }

  /**
   * Hash a reputation entry consistently
   */
  private hashEntry(entry: ReputationEntry): string {
    const data = JSON.stringify({
      address: entry.address.toLowerCase(),
      score: entry.score,
      attestations: entry.attestations.sort(),
      metadata: entry.metadata || {}
    });
    return keccak256(data).toString('hex');
  }

  /**
   * Get the merkle root
   */
  getRoot(): string {
    return '0x' + this.tree.getRoot().toString('hex');
  }

  /**
   * Generate a merkle proof for a given address
   */
  getProof(address: string): MerkleProof | null {
    const entry = this.entries.find(e => e.address.toLowerCase() === address.toLowerCase());
    if (!entry) return null;

    const leaf = this.hashEntry(entry);
    const leafIndex = this.leaves.indexOf(leaf);
    if (leafIndex === -1) return null;

    const proof = this.tree.getProof(leaf);
    
    return {
      leaf: '0x' + leaf,
      proof: proof.map(p => '0x' + p.data.toString('hex')),
      root: this.getRoot(),
      index: leafIndex
    };
  }

  /**
   * Verify a merkle proof
   */
  static verifyProof(proof: MerkleProof): boolean {
    try {
      const leafBuffer = Buffer.from(proof.leaf.slice(2), 'hex');
      const proofBuffers = proof.proof.map(p => Buffer.from(p.slice(2), 'hex'));
      const rootBuffer = Buffer.from(proof.root.slice(2), 'hex');
      
      return MerkleTree.verify(proofBuffers, leafBuffer, rootBuffer, keccak256, { sortPairs: true });
    } catch (error) {
      return false;
    }
  }

  /**
   * Get all entries in the tree
   */
  getEntries(): ReputationEntry[] {
    return [...this.entries];
  }

  /**
   * Get tree statistics
   */
  getStats(): { totalEntries: number; treeDepth: number; root: string } {
    return {
      totalEntries: this.entries.length,
      treeDepth: this.tree.getDepth(),
      root: this.getRoot()
    };
  }

  /**
   * Export tree data for persistence
   */
  export(): {
    entries: ReputationEntry[];
    leaves: string[];
    root: string;
    timestamp: string;
  } {
    return {
      entries: this.entries,
      leaves: this.leaves.map(leaf => '0x' + leaf),
      root: this.getRoot(),
      timestamp: new Date().toISOString()
    };
  }

  /**
   * Create tree from exported data
   */
  static fromExport(data: {
    entries: ReputationEntry[];
    leaves: string[];
    root: string;
    timestamp: string;
  }): ReputationMerkleTree {
    const tree = new ReputationMerkleTree(data.entries);
    
    // Verify the imported data matches
    if (tree.getRoot() !== data.root) {
      throw new Error('Imported tree root does not match calculated root');
    }
    
    return tree;
  }
}

export default ReputationMerkleTree;