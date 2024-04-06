# blockchain_miner.py

# DONT USE


import datetime
import hashlib
import json
import os
from blockchain import Blockchain, Block, Content, generate_key_pair, Transaction

class Miner:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def mine(self, transactions):
        difficulty = 4  # Set the difficulty level
        nonce = 0
        prefix = '0' * difficulty
        while True:
            # Serialize transactions to a list of dictionaries
            serialized_transactions = [tx.to_dict() for tx in transactions]
            # Serialize the list of dictionaries to JSON
            block_data = json.dumps(serialized_transactions) + str(nonce)
            hash_attempt = hashlib.sha256(block_data.encode()).hexdigest()
            if hash_attempt.startswith(prefix):
                return nonce, hash_attempt
            nonce += 1

if __name__ == "__main__":
    # Generate key pair
    private_key, public_key = generate_key_pair()

    # Convert public key to string
    public_key_str = public_key.decode('utf-8')

    # Initialize blockchain
    blockchain = Blockchain()

    # Initialize miner
    miner = Miner(blockchain)

    # Sample content
    content_data = Content("Sample Video", "This is a sample video", "Sample video data")

    # Create transaction
    transaction = Transaction(public_key_str, "recipient_public_key", 10)  # Example transaction with 10 units

    # Mine for content block
    nonce, content_hash = miner.mine([transaction])

    # Create content block
    content_block = Block(len(blockchain.chain), datetime.datetime.now(), [transaction], blockchain.get_latest_block().hash)
    content_block.nonce = nonce
    content_block.hash = content_hash

    # Add content block to blockchain
    blockchain.add_block(content_block)

    # Print data of latest block
    latest_block = blockchain.get_latest_block()
    print("Latest Block Data:")
    print("Index:", latest_block.index)
    print("Timestamp:", latest_block.timestamp)
    print("Transactions:")
    for transaction in latest_block.transactions:
        print("- Sender:", transaction.sender)
        print("  Recipient:", transaction.recipient)
        print("  Amount:", transaction.amount)
    print("Nonce:", latest_block.nonce)
    print("Previous Hash:", latest_block.previous_hash)
    print("Hash:", latest_block.hash)
