# blockchain.py

import json
import hashlib
import datetime
import os
import random
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

class Transaction:

    def __init__(self, sender, recipient, amount, data):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = datetime.datetime.now()
        self.data = data  # Additional data for the transaction
        self.hash = self.calculate_hash()  # Calculate and store the hash

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": str(self.timestamp),
            "data": self.data
        }

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update((self.sender + self.recipient + str(self.amount) + str(self.timestamp) + str(self.data)).encode('utf-8'))
        return sha.hexdigest()

    def is_valid(self):
        # Check if sender, recipient, amount, and data are present
        if not self.sender or not self.recipient or not self.amount or not self.data:
            return False
        # Check if the transaction hash matches the calculated hash
        if self.calculate_hash() != self.hash:
            return False
        return True

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0  # Nonce for Proof of Work
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update((str(self.index) + str(self.timestamp) + str(self.transactions) + str(self.previous_hash) + str(self.nonce)).encode('utf-8'))
        return sha.hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

    def is_valid(self, difficulty):
        # Check if the hash of the block meets the PoW difficulty criteria
        if self.hash[:difficulty] != '0' * difficulty:
            return False
        # Check if each transaction is valid
        for tx in self.transactions:
            if not tx.is_valid():
                return False
        return True

class Blockchain:
    MINING_REWARD = 10  # Reward for mining a block

    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.difficulty = 2
        self.directory = "blockchain_data"

        # Create directory if it doesn't exist
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def create_genesis_block(self):
        return Block(0, datetime.datetime.now(), [], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        if new_block.is_valid(self.difficulty) and new_block.previous_hash == self.get_latest_block().hash:
            self.chain.append(new_block)
            return True
        return False

    def receive_block(self, block_data):
        block = Block(
            block_data['index'],
            datetime.datetime.strptime(block_data['timestamp'], '%Y-%m-%d %H:%M:%S.%f'),
            [Transaction(
                tx['sender'],
                tx['recipient'],
                tx['amount'],
                tx['data']
            ) for tx in block_data['transactions']],
            block_data['previous_hash']
        )
        if self.add_block(block):
            print("Received block added to the chain.")
        else:
            print("Received block was not added to the chain.")

    def mine_pending_transactions(self, miner_address):
        if not self.pending_transactions:
            return False
        
        # Create a reward transaction for the miner
        reward_transaction = Transaction("SYSTEM", miner_address, self.MINING_REWARD, "Mining reward")
        self.pending_transactions.append(reward_transaction)

        new_block = Block(len(self.chain), datetime.datetime.now(), self.pending_transactions, self.get_latest_block().hash)
        new_block.mine_block(self.difficulty)
        
        if self.add_block(new_block):
            self.pending_transactions = []  # Clear pending transactions
            return True
        return False

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def is_valid(self):
        # Check if each block is valid
        for i in range(1, len(self.chain)):
            if not self.chain[i].is_valid(self.difficulty):
                return False
        
        # Check if the previous hash of each block matches the hash of the previous block
        for i in range(1, len(self.chain)):
            if self.chain[i].previous_hash != self.chain[i-1].hash:
                return False
        
        return True

    def save_to_file(self):
        blockchain_data = []
        for block in self.chain:
            block_data = {
                "index": block.index,
                "timestamp": str(block.timestamp),
                "transactions": [tx.to_dict() for tx in block.transactions],
                "previous_hash": block.previous_hash,
                "nonce": block.nonce,
                "hash": block.hash
            }
            blockchain_data.append(block_data)

        file_path = os.path.join(self.directory, "blockchain.json")
        with open(file_path, "w") as file:
            json.dump(blockchain_data, file, indent=4)

class Content:
    def __init__(self, title, description, content):
        self.title = title
        self.description = description
        self.content = content

    def publish(self, private_key):
        return {"title": self.title, "description": self.description, "content": self.content, "private_key": private_key}

def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_key_pem, public_key_pem
