# Imports
import json
import logging
import os
import sys
import threading
from socket import *
from time import strftime, localtime

# sort out logging
logging.basicConfig(filename='server.log',
                    filemode='a',
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    level=logging.DEBUG)

# Processing system arguments
if len(sys.argv) != 3:
    print('Incorrect amount of arguments given.')
    logging.critical('Incorrect amount of arguments given.')
    exit()

# Validate port argument
serverPort = 0
try:
    serverPort = int(sys.argv[2])
except ValueError:
    print('Server port not given as integer.')
    logging.critical('Server port not given as integer.')
    exit()

# Setup server socket, error handling for binding too.
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

try:
    serverSocket.bind((sys.argv[1], serverPort))
except OSError:
    print('Unavailable or busy port.')
    logging.critical('Unavailable or busy port.')
    exit()

serverSocket.listen(1)
print('The server is ready to receive')


def get_subdirectory_name_list(directory_name):
    """
    Returns a list of subdirectories in a directory.

    :param directory_name: The name of the directory to list the subdirectories of. Recommended to send a raw string.

    :returns: A list of directory names.
    """
    directory_list = []
    for directory in os.walk(directory_name):
        directory_list.append(directory[0][6:])  # removes the board/ and adds spaces
    return directory_list[1:]  # Skips the first one, as that is just board/


def get_board_messages(board_title):
    """
    Returns a list of the last 100 dictionaries containing the message title, timestamp, and the contents of a board

    :param board_title: The name of the directory to get the files from.
    :return: A list of dictionaries of the form { 'TITLE': <>, 'DATE': <>, 'TIMESTAMP': <>, 'DATA': <> }
        (title, time, data).
    """
    # Get file list
    if board_title == '':
        return {
            'ERROR': 'The board \'\' does not exist.'
        }
    try:
        file_list = os.listdir('{0}/{1}'.format('board', board_title))
    except FileNotFoundError:
        return {
            'ERROR': 'The board \'{0}\' does not exist.'.format(board_title)
        }
    # Sort it by most recent
    file_list.sort(reverse=True)
    # Pick the first 100
    file_list = file_list[:100]

    # Initialise our message list
    message_list = []
    for file in file_list:
        file_split = file.split("-")
        data = open('{0}/{1}/{2}'.format('board', board_title, file), 'r').read()
        message = {
            'TITLE': file_split[2].replace("_", " "),
            'DATE': file_split[0],
            'TIMESTAMP': file_split[1],
            'DATA': data
        }
        message_list.append(message)

    # Then return it
    return message_list


def new_post(board_title, post_title, post_content):
    """
    Creates a new post with given parameters.

    :param board_title: The board to post it to.
    :param post_title: The title of the post.
    :param post_content: The contents of the post.
    :return: Error if board does not exist, otherwise None.
    """
    if not os.path.isdir('{0}/{1}'.format('board', board_title)) or board_title == '':
        return {
            'ERROR': 'Board \'{0}\' does not exist.'.format(board_title)
        }
    else:
        # Create title of form YYYYMMDD-HHMMSS-<title>
        title = '{0}-{1}'.format(strftime('%Y%m%d-%H%M%S', localtime()), post_title)
        f = open('{0}/{1}/{2}'.format('board', board_title, title), 'w')
        f.write(post_content)
        f.close()
        return None


def handle_thread(socket, addr):
    """
    Called when a new connection is made.
    :param socket: the socket the data is coming from.
    :param addr: the address of the client.
    """
    receive_data = ""
    try:
        while True:
            receive_data = socket.recv(8192)
            if receive_data == b'':
                socket.close()
                break
            else:
                receive_data = json.loads(receive_data.decode())
                socket.send(handle_connection(receive_data, addr))
    finally:
        socket.close()


def handle_connection(receive_data, addr):
    """
    Called when a new request is received.
    :param receive_data: the decoded data received.
    :param addr: the address of the client (for logging).
    :return: the response.
    """
    response = ''
    if receive_data['COMMAND'] == 'GET_BOARDS':
        """ GET_BOARDS COMMAND """
        response = json.dumps({
            'DATA': get_subdirectory_name_list('board')
        })
        # Logging
        logging.info('GET_BOARDS {0} OK'.format(addr))

    elif receive_data['COMMAND'] == 'GET_MESSAGES':
        """ GET_MESSAGES COMMAND """
        if 'BOARD_TITLE' not in receive_data:
            # Missing parameter error
            response = json.dumps({
                'ERROR': 'Parameter missing: board title.'
            })
            # logging
            logging.error('GET_MESSAGES {0}'.format(addr))
        else:
            # No error
            board_message_list = get_board_messages(receive_data['BOARD_TITLE'].replace('/', '').replace('.', ''))
            if 'ERROR' in board_message_list:
                # If error in getting board messages
                response = json.dumps(board_message_list)
                # Error
                logging.error('GET_MESSAGES {0}'.format(addr))
            else:
                # No error
                response = json.dumps({
                    'DATA': board_message_list
                })
                # Logging
                logging.info('GET_MESSAGES {0} OK'.format(addr))
    elif receive_data['COMMAND'] == 'POST_MESSAGE':
        """ POST_MESSSAGE COMMAND"""
        # Check that all parameters are there
        missing_parameter_list = []
        if 'BOARD_TITLE' not in receive_data:
            missing_parameter_list.append('board title')
        if 'POST_TITLE' not in receive_data:
            missing_parameter_list.append('post title')
        if 'POST_CONTENT' not in receive_data:
            missing_parameter_list.append('post content')
        # Missing parameter(s) error
        if len(missing_parameter_list) > 0:
            parameter_text = ''
            for parameter in missing_parameter_list:
                parameter_text += '{0}, '.format(parameter)
            parameter_text = parameter_text[:-2]  # removing leading comma
            response = json.dumps({
                'ERROR': 'Parameter(s) missing: {0}.'.format(parameter_text)
            })
            # Logging
            logging.error('POST_MESSAGE {0}'.format(addr))
        else:
            # No missing parameters
            # Make a new post and check for error
            error = new_post(receive_data['BOARD_TITLE'], receive_data['POST_TITLE'], receive_data['POST_CONTENT'])
            if error is None:
                # No error
                response = json.dumps({
                    'DATA': 'Message posted successfully.'
                })
                # Logging
                logging.info('POST_MESSAGE {0} OK'.format(addr))
            else:
                # Error
                response = json.dumps(error)
                # Logging
                logging.error('POST_MESSAGE {0}'.format(addr))
    else:
        """ INVALID COMMAND """
        response = json.dumps({
            'ERROR': 'Invalid command'
        })
        logging.error('INVALID_COMMAND {0}'.format(addr))
    return response.encode()


while True:
    # Handle the threading so multiple clients can be handled.
    connection_socket, addr = serverSocket.accept()
    threading.Thread(target=handle_thread, args=(connection_socket, addr,)).start()
