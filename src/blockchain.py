"""
blockchain.py
=============
Educational Patient Records Blockchain (sanitized copy)

This is a cleaned version of the student demo showing a simple PoW blockchain
implementation used for storing patient-record-like payloads. It is suitable
for public sharing as part of a student portfolio.
"""

import hashlib
import time
import json


# BLOCK CLASS

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index         = index
        self.previous_hash = previous_hash
        self.timestamp     = timestamp
        self.data          = data
        self.nonce         = nonce
        self.hash          = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index":         self.index,
            "previous_hash": self.previous_hash,
            "timestamp":     self.timestamp,
            "data":          self.data,
            "nonce":         self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"  ✓ Block {self.index} mined | nonce={self.nonce} | hash={self.hash[:20]}...")

    def to_dict(self):
        return {
            "index":         self.index,
            "previous_hash": self.previous_hash,
            "timestamp":     self.timestamp,
            "data":          self.data,
            "nonce":         self.nonce,
            "hash":          self.hash
        }


# BLOCKCHAIN CLASS

class Blockchain:
    def __init__(self, difficulty=2):
        self.difficulty = difficulty
        self.chain = [self._create_genesis_block()]

    def _create_genesis_block(self):
        genesis = Block(
            index=0,
            previous_hash="0",
            timestamp=time.time(),
            data={"info": "Genesis Block — Student Demo"}
        )
        print(f"  ✓ Genesis block created | hash={genesis.hash[:20]}...")
        return genesis

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        new_block = Block(
            index=len(self.chain),
            previous_hash=self.get_latest_block().hash,
            timestamp=time.time(),
            data=data
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self, chain=None):
        if chain is None:
            chain = self.chain

        for i in range(1, len(chain)):
            current  = chain[i]
            previous = chain[i - 1]

            if current.hash != current.calculate_hash():
                print(f"  ✗ Block {i}: hash mismatch (tampered data)")
                return False

            if current.previous_hash != previous.hash:
                print(f"  ✗ Block {i}: broken chain link")
                return False

        return True

    def consensus(self, competing_chains):
        longest_chain = None
        max_length    = len(self.chain)

        for chain in competing_chains:
            if len(chain) > max_length and self.is_chain_valid(chain):
                max_length    = len(chain)
                longest_chain = chain
                print(f"  → Longer valid chain found: length {max_length}")

        if longest_chain:
            self.chain = longest_chain
            print("  ✓ Consensus: chain replaced with longest valid chain.")
            return True

        print("  ✓ Consensus: current chain is already the longest.")
        return False

    def display_chain(self):
        print("\n" + "="*70)
        print("  BLOCKCHAIN STATE")
        print("="*70)
        for block in self.chain:
            print(f"\n  Block #{block.index}")
            print(f"    Hash          : {block.hash}")
            print(f"    Previous Hash : {block.previous_hash}")
            print(f"    Nonce         : {block.nonce}")
            if isinstance(block.data, dict):
                for k, v in block.data.items():
                    print(f"    {k:16s}: {v}")
            else:
                print(f"    Data          : {block.data}")
        print("="*70 + "\n")


if __name__ == "__main__":

    print("\n" + "="*70)
    print("  Student Demo — Patient Records Blockchain")
    print("="*70)

    blockchain = Blockchain(difficulty=2)

    records = [
        {"patientName": "Patient A", "diagnosis": "Example", "treatment": "Demo", "provider": "Provider 1"},
        {"patientName": "Patient B", "diagnosis": "Example", "treatment": "Demo", "provider": "Provider 1"},
    ]

    print("\n--- Mining Patient Record Blocks ---")
    for record in records:
        print(f"\n  Mining: {record['patientName']} — {record['diagnosis']}")
        blockchain.add_block(record)
        print(f"  Chain valid: {blockchain.is_chain_valid()}")

    blockchain.display_chain()
