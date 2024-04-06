# Updated testnet.py
from blockchain import Blockchain, Block, Transaction, generate_key_pair
import random
import string
import time
import threading
import os
import fcntl
import json

def acquire_lock(file):
    """Acquire an exclusive lock on the file."""
    fcntl.flock(file.fileno(), fcntl.LOCK_EX)

def release_lock(file):
    """Release the lock on the file."""
    fcntl.flock(file.fileno(), fcntl.LOCK_UN)

def random_string(length=10):
    """Generate a random string of given length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_random_transactions(num_transactions):
    """Generate a list of random transactions."""
    transactions = []
    for _ in range(num_transactions):
        sender = random_string()
        recipient = random_string()
        amount = random.randint(1, 100)
        data = {"field1": random_string(), "field2": random_string()}  # Example additional data
        transaction = Transaction(sender, recipient, amount, data)
        transactions.append(transaction)
    return transactions

def mine_blocks(blockchain, lock):
    """Miner thread to mine pending transactions."""
    while True:
        time.sleep(5)  # Mine every 5 seconds
        with lock:
            if blockchain.mine_pending_transactions(miner_address="miner"):
                print("[Miner] Block mined successfully!")
                blockchain.save_to_file()
            else:
                print("[Miner] No pending transactions to mine.")

def main():
    # Initialize blockchain
    blockchain = Blockchain()

    # Create directory if it doesn't exist
    directory = "blockchain_data"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Open blockchain file
    file_path = os.path.join(directory, "blockchain.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            blockchain_data = json.load(file)
            if blockchain_data:
                blockchain.blocks = []
                for block_dict in blockchain_data:
                    index = block_dict.get("index")
                    timestamp = block_dict.get("timestamp")
                    previous_hash = block_dict.get("previous_hash")
                    nonce = block_dict.get("nonce")
                    transactions = block_dict.get("transactions", [])  # Default to empty list if key is missing
                    block = Block(index, timestamp, transactions, previous_hash)
                    blockchain.blocks.append(block)

    with open(file_path, "a+") as file:
        pass  # Create an empty file if it doesn't exist

    with open(file_path, "a") as file:
        # Acquire lock
        acquire_lock(file)

        # Start miner thread
        lock = threading.Lock()
        miner_thread = threading.Thread(target=mine_blocks, args=(blockchain, lock))
        miner_thread.start()

        try:
            while True:
                # Generate random transactions
                num_transactions = random.randint(1, 5)
                transactions = generate_random_transactions(num_transactions)

                # Add transactions to the blockchain
                with lock:
                    for transaction in transactions:
                        blockchain.add_transaction(transaction)
                        print("[Instance] Transaction added to pending transactions:", transaction.to_dict())

                time.sleep(3)  # Wait for transactions to accumulate
        except KeyboardInterrupt:
            print("\n[Instance] Exiting...")
            miner_thread.join()

if __name__ == "__main__":
    main()
