# Get the chat id (MAIN)
    This function prompts the user to send 'use this chat' message and obtaisns the chat id of the chat where the message was sent.
## Parameters
    - client : (TelegramClient) Client object to be used for login.

    - phone number : (str) Phone number of the user.
    
    - back up folders : (list) List of folders to be backed up.
## Returns
    db_dict["chat_id"]
         - chat_id : (int) Chat id of the chat where the message was sent.

# Messsage Handler
    This is that message handler that is called when a new message is received.
    It checks if the message contains required keywords and saves the chat id of the chat it received the message from. It also sends an acknowledgement to the same chat as well.

## Parameters
     - update : It is the update object that is passed to the message handler.

## Returns
    None
