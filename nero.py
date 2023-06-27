from telethon import TelegramClient, events, Button
from telethon.tl.functions.channels import GetFullChannelRequest, GetMessagesRequest
import time
import socks
import asyncio
import traceback
import logging
import csv
from collections import defaultdict
import random
from collections import deque


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set up the clients (ENTER YOUR OWN SESSION PROPERTIES!!!!!!)
api_id_1 = 22491024
api_hash_1 = '04c99c7dda9c00bc55b4111f1f86b1f1'
session_name_1 = '@AlexTheTrade1'

api_id_2 = 28191380
api_hash_2 = '5c5322179cbb67eb21fb4b012e3b6ade'
session_name_2 = '@beaverdigger'


api_id_3 = 28213222 
api_hash_3 = 'ffa7d53e8ed3eedf7de0c6561624e715'
session_name_3 = '@mishaesty'

api_id_4 = 24316363 
api_hash_4 = 'd085ae91c70415f74d3cb47813f8b20f'
session_name_4 = '@gleb31_03'
#

##
api_id_5 = 29762744 
api_hash_5 = '7b34f1016b4d4651ac0a325604570665'
session_name_5 = '@pmp_clcs' 

api_id_6 = 22227192 
api_hash_6 = '8b2ff6512e076fdac996c8ab058ab24e'
session_name_6 = '@renat0x12' 




#api_id_5 = 28213222
#api_hash_5 = 'ffa7d53e8ed3eedf7de0c6561624e715'
#session_name_5 = '@mishaesty' 
#

#invitebot5 is emanuel
# Your new mapping of clients to usernames
client_usernames = {
    'client_1': 'AlexTheTrade1',
    'client_2': 'beaverdigger',
    'client_3': 'mishaesty',
    'client_4': 'gleb31_03',
    'client_5': 'pmp_clcs',
    'client_6': 'renat0x12 '
}

source_group_id = -1001901654716 # The source group ID
#destination_group_ids = [-1001096132026,-1001385990821, -1001397091851,  -1001369722752,   -1001446433029,      -1001445225777] # Add all destination group IDs here
##                        DeChat         cscalpcrypto  nftcryptochat       cscalp        Tradeparty       chatik crypto daily


#destination_group_ids = 

                        #near
destination_group_ids = [-1001932220803]


                            #Gagarin_talk, proton_chatroom   beincrypto_ru    CRYPTUS_CHAT    dechat CryptosherlockClub  cmnchat         https://t.me/walken_io_ru
#destination_group_ids = [-1001284653961, -1001493667078, -1001450899936, -1001231516554, -1001096132026, -1001366308827, -1001496254455, -1001644915472]


#for tests
#destination_group_ids = [-1001951200089,-1001968851941]


#          @Katuin13  @Godzilaa26 @NIkit066 @DrozdPicker
our_bots = [6070484225,6212604875,6175528176,6250872430, 6191961101, 6265746098, 6285985823, 6278262373,5848233389,6063772078, 6266807770] #Our users' user_ids. Used to tell if someone replied to us.


# Set up the reply queue and lock
clients_for_reply = {}
last_message_ids = {}
# Define your proxy pools




proxy_pool_1 = [
    ('94.131.56.199', 59101, 'mbuloichyk', 'mUqLsKJ9Gk'),
    ('94.131.56.201', 59101, 'mbuloichyk', 'mUqLsKJ9Gk')
]

proxy_pool_2 = [
    ('94.131.56.202', 59101, 'mbuloichyk', 'mUqLsKJ9Gk'),
    ('94.131.56.56', 59101, 'mbuloichyk', 'mUqLsKJ9Gk')
]

proxy_pool_3 = [
    ('94.131.56.209', 59101, 'mbuloichyk', 'mUqLsKJ9Gk'),
    ('94.131.56.111', 59101, 'mbuloichyk', 'mUqLsKJ9Gk')
]

proxy_pool_4 = [
    ('95.164.145.58', 59101, 'mbuloichyk', 'mUqLsKJ9Gk'),
    ('94.131.56.153', 59101, 'mbuloichyk', 'mUqLsKJ9Gk')
]

proxy_pool_5 = [
    ('94.131.48.34', 59101, 'mbuloichyk', 'mUqLsKJ9Gk'),
    ('94.131.48.17', 59101, 'mbuloichyk', 'mUqLsKJ9Gk')
]

proxy_pool_6 = [
    ('23.27.3.51', 59101, 'mbuloichyk', 'mUqLsKJ9Gk'),
    ('23.27.3.248', 59101, 'mbuloichyk', 'mUqLsKJ9Gk')
]



# Add a message count and proxy index for each client
proxy_pool = {session_name_1: proxy_pool_1, session_name_2: proxy_pool_2, session_name_3: proxy_pool_3, session_name_4: proxy_pool_4, session_name_5: proxy_pool_5, session_name_6: proxy_pool_6}
proxy_indexes = {key: 0 for key in client_usernames.keys()}
message_counts = {key: 0 for key in client_usernames.keys()}


# In your data module
client_disconnect_flags = {
    'client_1': False,
    'client_2': False,
    'client_3': False,
    'client_4': False,
    'client_5': False,
    'client_6': False
}



#proxy_indexes = {key: 0 for key in client_usernames.keys()}
#message_counts = {key: 0 for key in client_usernames.keys()}
# Access the proxy pools using dot notation #Move it to the data in the future



# Create a list to hold clients that need to be disconnected
clients_to_disconnect = []
clients_to_reconnect = {}



last_messages_by_user = {}

message_counts = defaultdict(int) # Keep track of the message counts for each client

async def main():

     #Define your function to set up clients
    def setup_client(session_name, api_id, api_hash, proxy):
        proxy = (socks.SOCKS5, *proxy)
        client = TelegramClient(session_name, api_id, api_hash, proxy=proxy)
        return client
    # Define your function to set up clients

    
    # Create the clients 
    client_1 = setup_client(session_name_1, api_id_1, api_hash_1, proxy=proxy_pool_1[0])
    client_2 = setup_client(session_name_2, api_id_2, api_hash_2, proxy=proxy_pool_2[0])
    client_3 = setup_client(session_name_3, api_id_3, api_hash_3, proxy=proxy_pool_3[0])
    client_4 = setup_client(session_name_4, api_id_4, api_hash_4, proxy=proxy_pool_4[0])
    client_5 = setup_client(session_name_5, api_id_5, api_hash_5, proxy=proxy_pool_5[0])
    client_6 = setup_client(session_name_6, api_id_6, api_hash_6, proxy=proxy_pool_6[0])


    client_list = [client_1, client_2, client_3, client_4, client_5, client_6]
    client_last_messages = {client: None for client in client_list}

    clients = {
    'client_1': client_1,
    'client_2': client_2,
    'client_3': client_3,
    'client_4': client_4,
    'client_5': client_5,
    'client_6': client_6,
    }

    async def start_client(client, name):

        # If the client is already disconnected (according to our flags), we don't want to start it again
        if client_disconnect_flags[name]:
            logging.info(f"Client {name} is marked as disconnected, skipping start.")
            print(f"Client {name} is marked as disconnected, skipping start.")
            return
        try:
            await client.start()
            logging.info(f'{name} started and connected')
            print(f'{name} started and connected')
        except Exception as e:
            logging.error(f'Error with {name}: {e}')
            print(f'Error with {name}: {e}')
            # If the client is not marked as disconnected, it means this disconnect was unintentional and we want to reconnect
            if not client_disconnect_flags[name]:
                print(f'Restarting {name} in 5 seconds')
                logging.info(f'Restarting {name} in 5 seconds')
                await asyncio.sleep(5)  # wait for 5 seconds before attempting to reconnect
                await start_client(client, name)

    async def start_clients():
        await asyncio.gather(
            #print(f"starting client{client_1.session_name}"),
            start_client(client_1, 'client_1'),
            #print(f"starting client{client_2.session_name}"),
            start_client(client_2, 'client_2'),
            #print(f"starting client{client_3.session_name}"),
            start_client(client_3, 'client_3'),
            #print(f"starting client{client_4.session_name}"),
            start_client(client_4, 'client_4'),
            start_client(client_5, 'client_5'),
            start_client(client_6, 'client_6')
        )


    async def stop_client(client, name,):
        logging.debug(f"Starting to disconnect {name}")
        # First, we set the flag indicating this client is being intentionally disconnected
        client_disconnect_flags[name] = True
        logging.debug(f"Disconnecting {client.is_connected()}...")
        print(f'Is Client connected? - {client.is_connected()}')
        # Then, we disconnect the client
        logging.debug(f"Disconnecting {name}...")
        try:
            await client.disconnect()
            logging.debug(f"{name} disconnected")
        except OSError:
            print('Error on disconnect')
            logging.debug(f"{name} disconnected")
        except Exception as e:
            logging.exception(f"Error while disconnecting {name}: {e}")

        # After the client is disconnected, we can change the proxy
        # Get the next proxy for this client from the pool
        print(f'Is Client connected ater the disconnect? - {client.is_connected()}')
        proxy_indexes[name] = (proxy_indexes[name] + 1) % len(proxy_pool['@' + client_usernames[name]])
        new_proxy = proxy_pool['@' + client_usernames[name]][proxy_indexes[name]]
        print(f'New proxy for {name}: {new_proxy}')

        logging.debug(f"Setting new proxy for {name}: {new_proxy}")
        try:
            client.set_proxy(('socks5', new_proxy[0], new_proxy[1]))
            logging.debug(f"New proxy set for {name}")
        except Exception as e:
            logging.exception(f"Error while setting new proxy for {name}: {e}")

        # Now, we unset the disconnect flag so that the client can be reconnected in start_client()
        client_disconnect_flags[name] = False
        logging.debug(f"Finished disconnecting and changing proxy for {name}")

   

    async def handle_new_message(event, client_name, client, source_group_id):
        # Define the limit of messages to be sent before changing the proxy
        K = 1
        client_username = client_usernames[client_name]
        # Get the message text and the tagged username
        message_text = event.message.message
        tag_index = message_text.find('@' + client_username)
        message_text = message_text[tag_index + len('@' + client_username):].strip()
        # Increment the count of messages for this client
        message_counts[client_name] += 1
        # Check if the message limit has been reached for this client
        # Increment the count of messages for this client
    # Check if the message limit has been reached for this client
        if message_counts[client_name] >= 4:
            # Reset the message count for this client
            message_counts[client_name] = 0
            # Disconnect and reconnect the client
            clients_to_reconnect[client_name] = (client, event, message_text)
            #await handle_client_reconnection(client, client_name)
            # After the client is reconnected, send the message
            return 
        else:
            # Check if the new message contains media
            image_path = None
            if event.message.media:
                image_path = await client.download_media(event.message.media)
            # Send the message normally
            await send_messages(event, client, client_name, message_text, source_group_id, image_path)


    async def check_clients_to_reconnect():
        while True:
            for client_name, (client, event, message_text) in list(clients_to_reconnect.items()):
                logging.debug(f'Checking reconnection for {client_name}')
                await handle_client_reconnection(client, client_name, message_text)
                

                # Call send_messages() with the stored event object
                await send_messages(event, client, client_name, message_text, source_group_id)
                # Remove this client from the clients_to_reconnect dictionary
                del clients_to_reconnect[client_name]

            await asyncio.sleep(10)  # Check for clients to reconnect every 10 seconds


            

    async def handle_client_reconnection(client, client_name, message_text):
        logging.debug(f'Handling reconnection for {client_name}')
        await stop_client(client, client_name)
        # Ensure the client is fully disconnected before proceeding
        #await client.disconnected
        await start_client(client, client_name)
        #clients_to_reconnect.remove((client, client_name, message_text)) 

#
    #async def send_messages(event, client, client_name, message_text,source_group_id):
    #    global message_counts
    #    message_counts[client_name] += 1
#
    #    for dest_group_id in destination_group_ids:
    #        # Ensure that every dest_group_id has a dictionary as value
    #        if dest_group_id not in last_message_ids or isinstance(last_message_ids[dest_group_id], int):
    #            last_message_ids[dest_group_id] = {'id': None, 'reply_to_msg_id': None}
#
    #         # Obtain reply_to from the source group if available
    #        reply_to_source = last_message_ids.get(source_group_id, {}).get('reply', {}).get('id', None)
    #        #DELAY BEFORE FORWARDING TO GROUPS 
    #        await asyncio.sleep(3)
    #        try:
    #            # Add debug statement here
    #            group_info = await event.client(GetFullChannelRequest(dest_group_id))
    #            print(f"Preparing to send message to group {group_info.chats[0].title} ({dest_group_id})")
    #            if clients_for_reply:
    #                for key in clients_for_reply:
    #                    await asyncio.sleep(1)
    #                    # If there is a previous message ID, reply to it
    #                    reply_queue, previous_message_id = clients_for_reply[key]
    #                   
    #                    reply_to = reply_to_source or last_message_ids[dest_group_id].get('reply_to_msg_id', last_message_ids[dest_group_id].get('id'))
    #                    print(f"Sending message '{message_text}' to group {dest_group_id} from client {client_name}  in reply to message {reply_to}")
    #                    sent_message = await client.send_message(dest_group_id, message_text, link_preview=False, reply_to=reply_to)
    #                    last_message_ids[dest_group_id] = {'id': sent_message.id, 'reply_to_msg_id': sent_message.reply_to_msg_id}
    #                    clients_for_reply[key] = (reply_queue + [sent_message.id], sent_message.id)
    #            else:
    #                await asyncio.sleep(5)
    #                # If there is no previous ID, just send the message
    #                print(f"Sending message '{message_text}' to group {dest_group_id} from client {client_name} as ")
    #                print(f"Client {client_name} has sent {message_counts[client_name]} messages so far")
    #                sent_message = await client.send_message(dest_group_id, message_text, link_preview=False)
    #                #wait client.send_message(source_group_id, )
    #                last_message_ids[dest_group_id] = {'id': sent_message.id, 'reply_to_msg_id': sent_message.reply_to_msg_id}
    #                clients_for_reply[client_name] = ([sent_message.id], sent_message.id)
    #        except Exception as e:
    #            print("Error: "+ str(e))

    #SEN_MESSAGES function to reply only to our bots.


    # shared reply queue
    reply_queues = defaultdict(deque)

    async def send_messages(event, client, client_name, message_text, source_group_id, image_path=None):
        for dest_group_id in destination_group_ids:
            # Add a delay before sending a message to a new destination group
            delay = random.randint(3, 7)  # Random delay between 3 and 7 minutes, in seconds
            await asyncio.sleep(delay)
            try:
                group_info = await event.client(GetFullChannelRequest(dest_group_id))
                print(f"Preparing to send message to group {group_info.chats[0].title} ({dest_group_id})")

                # pull a message id from the reply queue to reply to
                reply_to_id = None
                #if len(reply_queues[dest_group_id]) > 0:
                #    reply_to_id = reply_queues[dest_group_id].popleft()

                
                # If image_path is set, include the image in the sent message
                if image_path is not None:
                    sent_message = await client.send_file(dest_group_id, file=image_path, caption=message_text, reply_to=reply_to_id)
                else:
                    sent_message = await client.send_message(dest_group_id, message_text, link_preview=False, reply_to=reply_to_id)


                print(f"Sending message '{message_text}' to group {dest_group_id} from client {client_name} in reply to message {reply_to_id}")
                #sent_message = await client.send_message(dest_group_id, message_text, link_preview=False, reply_to=reply_to_id)

                

                # push this message id to the reply queue
                #reply_queues[dest_group_id].append(sent_message.id)

                # update the last message id
                last_message_ids[dest_group_id] = {'id': sent_message.id, 'reply_to_msg_id': sent_message.reply_to_msg_id}


            except Exception as e:
                print("Error: "+ str(e))
        print(f"Client {client_name} has sent the message '{message_text}' to all destination groups.")
        #await client.send_message(source_group_id, f"Client {client_name} has sent the message '{message_text}' to all destination groups.")


    async def handle_reply(client, event, our_bots, source_group_id):
        try:
            # Checks if message is a reply
            if event.reply_to_msg_id:
                original_msg = await event.get_reply_message()
                if original_msg is not None and hasattr(original_msg.from_id,'user_id') and event.sender_id in our_bots:
                    print("Özümüzküdü")
                else:    

                    #If someone replied to the one of the bots, forward info to the source group(RUFS)            
                    if original_msg is not None and original_msg.from_id.user_id == (await client.get_me()).id:
                        chat = await event.get_chat()                    
                        sender = await event.get_sender()
                        if event.message.reply_to_msg_id:
                            msg_link = f"https://t.me/{chat.username}/{event.id}"
                        username = sender.username if sender.username else f"{sender.first_name} {sender.last_name}"
                        message_text = event.message.message
                        from_chat = chat.title

                        await client.send_message(source_group_id,f"User @{username} replied to my automated message from the group: {from_chat}. Message: {message_text}. Message link: {msg_link}")        
                        if source_group_id not in last_message_ids:
                            last_message_ids[source_group_id] = {}
                        last_message_ids[source_group_id]['reply'] = {'id': event.id, 'reply_to_msg_id': event.reply_to_msg_id}
        except Exception as e: 
            print(f"Error handling event: {e}")



    def read_script(file_name):
        with open(file_name, 'r') as f:
            reader = csv.reader(f)
            script = list(reader)
        return   script
    

    async def send_messages_by_script(event, client, user_name, message_text, group_id):
        await client.send_message(group_id, message_text)
        message_counts[user_name] += 1
        await asyncio.sleep(random.randint(1, 5)) # Sleep for a random time interval between 1 and 5 seconds


    async def start_conversation(event):
        script = read_script('conversation_script.csv')  
        for line in script:
            user_name, message_text = line  
            client_key = [key for key, value in client_usernames.items() if value == user_name][0]
            client = clients[client_key]  # Get the client based on the user_name
            # Send the message normally
            if message_counts[client_key] >= 4:  # Replace K with your desired limit
                # Reset the message count for this client
                message_counts[client_key] = 0
                # Disconnect and reconnect the client
                clients_to_reconnect[client_key] = (client, event, message_text)
                return
            else: 
                await send_messages_by_script(event, client, user_name, message_text, source_group_id)
                # Check if the message limit has been reached for this client
                
    


    async def handle_reply_client1(event):
        await handle_reply(client_1, event, our_bots, source_group_id)
    async def handle_reply_client2(event):
        await handle_reply(client_2, event, our_bots, source_group_id)
    async def handle_reply_client3(event):
        await handle_reply(client_3, event, our_bots, source_group_id)
    async def handle_reply_client4(event):
        await handle_reply(client_4, event, our_bots, source_group_id)
    async def handle_reply_client5(event):
        await handle_reply(client_5, event, our_bots, source_group_id)
    async def handle_reply_client6(event):
        await handle_reply(client_6, event, our_bots, source_group_id)

    async def run_client_until_disconnected(client):
            await client.run_until_disconnected()

    async def run_all_clients_until_disconnected():
        await asyncio.gather(
            run_client_until_disconnected(client_1),
            run_client_until_disconnected(client_2),
            run_client_until_disconnected(client_3),
            run_client_until_disconnected(client_4),
            run_client_until_disconnected(client_5),
            run_client_until_disconnected(client_6)
        )


    async def handle_reset_queue(event):
        global clients_for_reply
        global last_message_ids
        clients_for_reply = {}
        last_message_ids = {}
        await event.respond('Response chronology has been reset. Your next message will not be a reply. After, clients will continue replying to each other as it was.')

    #start clients
    await start_clients()

    # Add the task to check for clients to disconnect
    
    asyncio.create_task(check_clients_to_reconnect())

    

    async def handle_client_1_message(event):
        await handle_new_message(event, 'client_1', client_1, source_group_id)

    async def handle_client_2_message(event):
        await handle_new_message(event, 'client_2', client_2, source_group_id)

    async def handle_client_3_message(event):
        await handle_new_message(event, 'client_3', client_3, source_group_id)

    async def handle_client_4_message(event):
        await handle_new_message(event, 'client_4', client_4, source_group_id)

    async def handle_client_5_message(event):
        await handle_new_message(event, 'client_5', client_5, source_group_id)

    async def handle_client_6_message(event):
        await handle_new_message(event, 'client_6', client_6, source_group_id)      
    
    
    # Define the handlers for each client   
    client_1.add_event_handler(
    handle_client_1_message,
    events.NewMessage(chats=source_group_id, pattern=r'@AlexTheTrade1(\w*)'))
    
    client_2.add_event_handler(
    handle_client_2_message,
    events.NewMessage(chats=source_group_id, pattern=r'@beaverdigger(\w*)'))

    client_3.add_event_handler(
    handle_client_3_message,
    events.NewMessage(chats=source_group_id, pattern=r'@mishaesty(\w*)'))

    client_4.add_event_handler(
    handle_client_4_message,
    events.NewMessage(chats=source_group_id, pattern=r'@gleb31_03(\w*)'))

    client_5.add_event_handler(
    handle_client_5_message,
    events.NewMessage(chats=source_group_id, pattern=r'@pmp_clcs(\w*)')) 

    client_6.add_event_handler(
    handle_client_6_message,
    events.NewMessage(chats=source_group_id, pattern=r'@renat0x12(\w*)')) 

    client_1.add_event_handler(
    handle_reset_queue,
    events.NewMessage(chats=source_group_id, pattern=r'@sbros'))

    # Add the handler for starting the conversation
    client_1.add_event_handler(
    start_conversation,
    events.NewMessage(chats=source_group_id, pattern='@start_conversation'))


    #Add handlers
    client_1.add_event_handler(handle_reply_client1,events.NewMessage(chats=destination_group_ids, incoming=True))
    client_2.add_event_handler(handle_reply_client2,events.NewMessage(chats=destination_group_ids, incoming=True))
    client_3.add_event_handler(handle_reply_client3,events.NewMessage(chats=destination_group_ids, incoming=True))
    client_4.add_event_handler(handle_reply_client4,events.NewMessage(chats=destination_group_ids, incoming=True))
    client_5.add_event_handler(handle_reply_client5,events.NewMessage(chats=destination_group_ids, incoming=True))
    client_6.add_event_handler(handle_reply_client6,events.NewMessage(chats=destination_group_ids, incoming=True))


    await run_all_clients_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())