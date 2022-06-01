import datetime
import json
import sys
from socket import *

# Date time format of incoming data to format it.
date_time_format = '%Y%m%d-%H%M%S'


def format_date_time(date_time):
    """
    Converts date to a nice readable form.
    :param date_time: date in the form %Y%m%d-%H%M%S
    :return: date in the format %Y/%m/%d %H:%M:%S
    """
    return datetime.datetime.strftime(datetime.datetime.strptime(date_time, date_time_format), '%Y/%m/%d %H:%M:%S')


# Argument existence check
if len(sys.argv) != 3:
    print('Incorrect amount of arguments given.')
    exit()

# Validating server port
serverPort = 0
try:
    serverPort = int(sys.argv[2])
except ValueError:
    print('Server port not given as integer.')
    exit()

serverName = sys.argv[3]
clientSocket = socket(AF_INET, SOCK_STREAM)

# Error checking for opening the socket.
try:
    clientSocket.connect((serverName, serverPort))
except ConnectionRefusedError:
    print('Server is not running or is unavailable.')
    exit()

print('Connected to the server successfully.')

# Get boards
request = {
    'COMMAND': 'GET_BOARDS'
}
clientSocket.send(json.dumps(request).encode())
# Get and decode the data
board_list = json.loads(clientSocket.recv(1024).decode())['DATA']

# Print the boards
print("---  BOARDS ---")
for i in range(0, len(board_list)):
    print('{0}: {1}'.format(i + 1, board_list[i].replace('_', ' ')))

# Take user input.
print()
user_input = input('> ')
print()

# Form user request
request = {}
if user_input == 'QUIT':
    clientSocket.close()
    exit()
elif user_input in [str(i) for i in range(1, len(board_list) + 1)]:
    # If a number from the list

    # Calculate index in board_list
    index = int(user_input) - 1

    # Build the request
    request = {
        'COMMAND': 'GET_MESSAGES',
        'BOARD_TITLE': board_list[index]
    }

    # Send the request
    clientSocket.send(json.dumps(request).encode())

    # Get the response
    response = json.loads(clientSocket.recv(8192).decode())

    # Check for errors
    if 'ERROR' in response:
        print(response['ERROR'])
        exit()

    # Print a confirmation
    print('Got the messages successfully.')

    # Reverse the message list (so new things are printed last, and show up first)
    response['DATA'].reverse()

    # Print each message
    for message in response['DATA']:
        print('_' * 19)
        print(format_date_time('{0}-{1}'.format(message['DATE'], message['TIMESTAMP'])))
        print()
        print('| TITLE\n  ', message['TITLE'], sep='')
        print()
        print('| MESSAGE\n  ', message['DATA'], sep='')
        print()
elif user_input == 'POST':
    # Get the board index
    print('Which board would you like to post to?')
    board_number = input('> ')
    if board_number not in [str(i) for i in range(1, len(board_list) + 1)]:
        print('No board with that number exists.')
        exit()
    board_index = int(board_number) - 1

    # Get the post title
    print('\nWhat is your post title?')
    post_title = input('> ')

    # Get the post message
    print('\nWhat is your post message?')
    post_content = input('> ')

    # Lets build our request
    request = {
        'COMMAND': 'POST_MESSAGE',
        'BOARD_TITLE': board_list[board_index],
        'POST_TITLE': post_title.replace(' ', '_'),
        'POST_CONTENT': post_content
    }

    # Send our request
    clientSocket.send(json.dumps(request).encode())

    # Get our response
    response = json.loads(clientSocket.recv(1024).decode())

    # Error handling
    if 'ERROR' in response:
        print(response['ERROR'])
        exit()

    # Print our response
    print(response['DATA'])
else:
    # Invalid command
    print('Invalid command.')
    exit()
