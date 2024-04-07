import asyncio
import json
from blockchain import Blockchain
import socket

def get_ip_address():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # Connect to a remote server (doesn't matter which one)
        s.connect(("8.8.8.8", 80))
        
        # Get the IP address
        ip_address = s.getsockname()[0]
    except Exception as e:
        print("Error:", e)
        ip_address = None
    finally:
        # Close the socket
        s.close()
    
    return ip_address

MY_ADDRESS = get_ip_address()
opened = []
connected = []
check = []
checked = []
checking = False
temp_chain = Blockchain()

async def handle_handshake(message, writer):
    nodes = message['data']['nodes']
    nodes.insert(0, MY_ADDRESS)
    for node in nodes:
        if node in opened:
            print("alredy exists")
        elif node == MY_ADDRESS:
            print("my address")
        else:
            opened.append(node)
            reader, writer = await asyncio.open_connection(
            node, 8888)
            message = json.dumps({'type': 'HANDSHAKE', 'data': {'nodes': nodes}})
            writer.write(message.encode())
            connected.append(node)
            writer.close()


async def handle_create(message, writer):
    trasaction = message['data']
    temp_chain.add_transaction(trasaction)

async def handle_add(message, writer):
    new_block, new_diff = message['data']


async def handle_request_check(message, writer):
    for i in len(temp_chain.chain):
        message = json.dumps[{'type': 'SEND_CHAIN', 'data': 
                              {'block': temp_chain.chain[i], 
                               'finished': i == len(temp_chain.chain) -1}
                              }]
    writer.write(message.encode())
    writer.close()


async def handle_request_info(message, writer):
    for i in len(temp_chain.chain):
        message = json.dumps({'type': 'SEND_INFO', 'data': 
                              [temp_chain.difficulty, temp_chain.pending_transactions]})
    writer.write(message.encode())
    writer.close()
 
async def handle_send_check(message):
    if checking:
        check.append(message['data'])


async def start_listen():
    server = await asyncio.start_server(
        handle_message, '127.0.0.1', 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

async def handle_message(reader, writer):
    data = reader.read().decode('utf-8')
    message = json.loads(data)
    type = message['type']
    if(type == "HANDSHAKE"):
        await handle_handshake(message, writer)
    elif (type == "CREATE"):
        handle_create(message, writer)
    elif (type == "ADD"):
        handle_add(message, writer)
    elif (type == "REQUEST_CHAIN"):
        handle_request_check(message, writer)
    elif (type == "SEND_CHAIN"):
        handle_send_check(message, writer)
    elif (type == "REQUEST_INFO"):
        handle_request_info(message, writer)
    elif ( type == "SEND_INFO"):
        handle_send_check(message, writer)

asyncio.run(start_listen())