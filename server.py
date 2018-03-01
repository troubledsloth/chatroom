import socket
import time
import serverConfig
from threading import Thread

listOfUsers = []

IP = serverip
path = PATH

listeningPort = 5000
recievingPort = 5001
sendingPort = 5002

listeningSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recievingSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sendingSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

listeningSocket.bind((IP, listeningPort))
recievingSocket.bind((IP, recievingPort))

def listening():
    '''Waits for the a client to send its data( the IP address)
    which is added to listOfUsers. Also sends past chat history
    to new client'''
    global listOfUsers
    while True:
        data, addr = listeningSocket.recvfrom(4096)
        data = data.decode('utf-8')

        if data not in listOfUsers:
            listOfUsers.append(data)
        else:
            pass
        with open(path, 'r') as file:
            for line in file.readlines():
                line = line.replace('\n', '')
                line = line.encode()

                sendingSocket.sendto(line, (data, sendingPort))

        sendingSocket.sendto('''\nPast chat history loaded.
Please do not spam!
Enter anything to send to the chatroom. Enter "end" to quit.\n'''.encode(), (data, sendingPort))

def reciever():
    '''Waits to recieve incoming messages. Once a message is recieved, this
    function sends the message to every IP address in listOfUsers'''
    while True:
        data, addr = recievingSocket.recvfrom(4096)
        data = data.decode('utf-8')
        with open(path, 'a') as file:
            file.write(data + '\n')
        print(data)
        print('All users: {0} '.format(listOfUsers))


        data = data.encode()

        for ip in listOfUsers:

            sendingSocket.sendto(data, (ip, sendingPort))

def sendServerMessage():
    while True:
        message = input()
        message = 'Server Admin: {0}' .format(message)
        print(message)
        message = message.encode()
        for ip in listOfUsers:
            sendingSocket.sendto(message, (ip, sendingPort))



def main():
    t1 = Thread(target= listening, args=())
    t2 = Thread(target= reciever, args=())
    t3 = Thread(target= sendServerMessage, args=())
    t1.daemon = True
    t2.daemon = True
    t3.daemon = True
    t1.start()
    t2.start()
    t3.start()
    while True:
        time.sleep(60)



if __name__ == '__main__':
    with open(path, 'r') as file:
        for line in file.readlines():
            line = line.replace('\n', '')
            print(line)
    print('\nServer started... \n')
    main()