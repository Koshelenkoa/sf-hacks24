import asyncio
import json
import random
import string
import time
from blockchain import Blockchain, Block, Transaction

# Provided IP addresses
NODE_ADDRESSES = ['192.168.1.124', '192.168.1.137', '192.168.1.141', '192.168.1.137']

opened = []
connected = []
check = []
checked = []
checking = False
temp_chain = Blockchain()

async def handle_handshake(message, writer):
    nodes = message['data']['nodes']
    sender_ip = writer.get_extra_info('peername')[0]
    print(f"Received handshake from {sender_ip}")
    nodes.insert(0, sender_ip)  # Get the IP address of the connected node
    for node in nodes:
        if node in opened:
            print("Node already exists.")
        else:
            opened.append(node)
            try:
                reader, writer = await asyncio.open_connection(node, 8888)
                message = json.dumps({'type': 'HANDSHAKE', 'data': {'nodes': nodes}})
                writer.write(message.encode())
                connected.append(node)
                print(f"Connected to {node}")
                writer.close()
            except ConnectionRefusedError:
                print(f"Connection to {node} failed.")

async def handle_create(message, writer):
    print("Received create message")
    transaction_data = message['data']
    transaction = Transaction(transaction_data['sender'], transaction_data['recipient'], transaction_data['amount'], transaction_data['data'])
    temp_chain.add_transaction(transaction)

async def handle_add(message, writer):
    print("Received add message")
    new_block_data = message['data']
    new_block = Block(
        index=new_block_data['index'],
        timestamp=new_block_data['timestamp'],
        transactions=new_block_data['transactions'],
        previous_hash=new_block_data['previous_hash']
    )
    
    # Add the new block to the blockchain
    if temp_chain.add_block(new_block):
        print("New block added to the blockchain.")
        response_message = json.dumps({'type': 'ADD_SUCCESS', 'data': 'New block added successfully.'})
    else:
        print("Failed to add new block to the blockchain.")
        response_message = json.dumps({'type': 'ADD_ERROR', 'data': 'Failed to add new block.'})
    
    writer.write(response_message.encode())
    await writer.drain()
    writer.close()

async def handle_request_check(message, writer):
    print("Received request for chain")
    for i in range(len(temp_chain.chain)):
        message = json.dumps({'type': 'SEND_CHAIN', 'data': {'block': temp_chain.chain[i].__dict__, 'finished': i == len(temp_chain.chain) - 1}})
        writer.write(message.encode())
        await writer.drain()
    writer.close()

async def handle_request_info(message, writer):
    print("Received request for info")
    message = json.dumps({'type': 'SEND_INFO', 'data': {'difficulty': temp_chain.difficulty, 'pending_transactions': [tx.__dict__ for tx in temp_chain.pending_transactions]}})
    writer.write(message.encode())
    await writer.drain()
    writer.close()

async def handle_send_check(message):
    print("Received send check message")
    if checking:
        check.append(message['data'])

async def start_listen():
    server = await asyncio.start_server(handle_message, '0.0.0.0', 8888)  # Listen on all available interfaces

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

async def handle_message(reader, writer):
    data = await reader.read()
    message = json.loads(data.decode('utf-8'))
    message_type = message['type']
    print(f"Received message of type: {message_type}")
    if message_type == "HANDSHAKE":
        await handle_handshake(message, writer)
    elif message_type == "CREATE":
        await handle_create(message, writer)
    elif message_type == "ADD":
        await handle_add(message, writer)
    elif message_type == "REQUEST_CHAIN":
        await handle_request_check(message, writer)
    elif message_type == "SEND_CHAIN":
        await handle_send_check(message)
    elif message_type == "REQUEST_INFO":
        await handle_request_info(message, writer)
    elif message_type == "SEND_INFO":
        await handle_send_check(message)

async def generate_random_transactions(num_transactions):
    """Generate a list of random transactions."""
    transactions = []
    for _ in range(num_transactions):
        sender = ''.join(random.choices(string.ascii_lowercase, k=5))
        recipient = ''.join(random.choices(string.ascii_lowercase, k=5))
        amount = random.randint(1, 100)
        data = {"field1": ''.join(random.choices(string.ascii_lowercase, k=10)), "field2": ''.join(random.choices(string.ascii_lowercase, k=10))}  # Example additional data
        transaction = Transaction(sender, recipient, amount, data)
        transactions.append(transaction)
    return transactions

async def mine_blocks(blockchain):
    """Miner thread to mine pending transactions."""
    while True:
        await asyncio.sleep(5)  # Mine every 5 seconds
        if blockchain.pending_transactions:
            print("[Miner] Mining new block...")
            if blockchain.mine_pending_transactions(miner_address="miner"):
                print("[Miner] Block mined successfully!")
                blockchain.save_to_file()
            else:
                print("[Miner] No pending transactions to mine.")

async def main():
    # Start miner task
    miner_task = asyncio.create_task(mine_blocks(temp_chain))

    # Simulate generating and adding random transactions
    try:
        while True:
            await asyncio.sleep(3)  # Wait for transactions to accumulate
            num_transactions = random.randint(1, 5)
            transactions = await generate_random_transactions(num_transactions)
            print("[Instance] Adding transactions to pending transactions...")
            for transaction in transactions:
                temp_chain.add_transaction(transaction)
                print("[Instance] Transaction added to pending transactions:", transaction.to_dict())
    except KeyboardInterrupt:
        print("\n[Instance] Exiting...")
        miner_task.cancel()

if __name__ == "__main__":
    asyncio.run(start_listen())
    asyncio.run(main())
