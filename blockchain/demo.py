import asyncio
import json
import random
import string
import time
from blockchain import Blockchain, Block, Transaction
import socket
import requests


hostname = socket.gethostname()
MY_ADDRESS = socket.gethostbyname(hostname)

# Provided IP addresses
NODE_ADDRESSES = ['192.168.1.137', '192.168.1.141']
PORT = 8888
WEB_ADDRESS = '127.0.0.1' #local testing
WEB_PORT = 80

opened = []
connected = []
check = []
checked = []
checking = False
temp_chain = Blockchain()

async def get_ips(): #request ips from the central server
    url = f"http://{WEB_ADDRESS}/{WEB_PORT}/ips" 

    response = requests.get(url)

    if response.status_code == 200:
        ips = response.json()
        NODE_ADDRESSES = set(NODE_ADDRESSES).union(set(ips))
    else:
    # Print an error message
        print("Error:", response.status_code)

async def broadcast(message):
    for node in NODE_ADDRESSES:
        if node != MY_ADDRESS:
            reader, writer = await asyncio.open_connection(node, PORT)
            writer.write(message.encode())
            connected.append(node)
            print(f"Connected to node: {node}")
            writer.close()


async def connect_to_nodes():
    """Establish connections to other nodes."""
    for node_address in NODE_ADDRESSES:
        try:
            reader, writer = await asyncio.open_connection(node_address, PORT)
            message = json.dumps({'type': 'HANDSHAKE', 'data': {'nodes': NODE_ADDRESSES}})
            writer.write(message.encode())
            connected.append(node_address)
            print(f"Connected to node: {node_address}")
            writer.close()
        except ConnectionRefusedError:
            print(f"Connection to node {node_address} failed.")

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
                reader, writer = await asyncio.open_connection(node, PORT)
                message = json.dumps({'type': 'HANDSHAKE', 'data': {'nodes': nodes}})
                writer.write(message.encode())
                connected.append(node)
                print(f"Connected to {node}")
                writer.close()
            except ConnectionRefusedError:
                print(f"Connection to {node} failed.")

async def handle_create(message, writer):
    transaction_data = message['data']
    transaction = Transaction(transaction_data['sender'], transaction_data['recipient'], transaction_data['amount'], transaction_data['data'])
    temp_chain.add_transaction(transaction)

async def handle_add(message, writer):
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
        message_res = json.dumps({'type': 'REQUEST_CHECK', 'data': MY_ADDRESS})
        broadcast(message_res)
    else:
        print("Failed to add new block to the blockchain.")

async def handle_request_check(message, writer):
    for i in range(len(temp_chain.chain)):
        message = json.dumps({'type': 'SEND_CHAIN', 'data': {'block': temp_chain.chain[i].__dict__, 'finished': i == len(temp_chain.chain) - 1}})
        writer.write(message.encode())
        await writer.drain()
    writer.close()

async def handle_request_info(message, writer):
    message = json.dumps({'type': 'SEND_INFO', 'data': {'difficulty': temp_chain.difficulty, 'pending_transactions': [tx.__dict__ for tx in temp_chain.pending_transactions]}})
    writer.write(message.encode())
    await writer.drain()
    writer.close()

async def handle_send_check(message):
    if checking:
        check.append(message['data'])

async def start_listen():
    server = await asyncio.start_server(handle_message, '0.0.0.0', PORT)  # Listen on all available interfaces

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

async def handle_message(reader, writer):
    data = await reader.read()
    message = json.loads(data.decode('utf-8'))
    message_type = message['type']
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

async def add_random_transactions():
    """Add random transactions to the blockchain."""
    while True:
        sender = ''.join(random.choices(string.ascii_letters, k=10))
        recipient = ''.join(random.choices(string.ascii_letters, k=10))
        amount = random.randint(1, 100)
        data = {'sender': sender, 'recipient': recipient, 'amount': amount, 'data': ''}
        transaction = Transaction(**data)
        temp_chain.add_transaction(transaction)
        broadcast(json.dumps({'type': 'CREATE', 'data': {'sender': sender, 'recipient': recipient, 'amount': amount}})) 
        await asyncio.sleep(5)  # Add transaction every 5 seconds

async def mine_blocks():
    """Mine blocks for the blockchain."""
    while True:
        if len(temp_chain.pending_transactions) > 0:
            new_block = temp_chain.mine_block()
            print("New block mined!")
        await asyncio.sleep(10)  # Mine a block every 10 seconds

if __name__ == "__main__":
    asyncio.run(asyncio.gather(connect_to_nodes(), start_listen(), add_random_transactions(), mine_blocks()))
