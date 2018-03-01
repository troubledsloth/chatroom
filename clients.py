import socket, sys, os, datetime, time
from threading import Thread


name = os.getlogin()

ServerIP = '192.168.1.128'
hostIP = socket.gethostbyname(socket.gethostname())

initialisationPort = 5000
sendingPort = 5001
recievingPort = 5002

initialisationSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sendingSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recievingSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

recievingSocket.bind((hostIP, recievingPort))


def initialisation():
    '''Function runs once. Sends this machine's IP address to the server
    Also recieves all past chat history'''
    hostIPCopy = hostIP.encode('utf-8')
    initialisationSocket.sendto(hostIPCopy, (ServerIP, initialisationPort))



def sender():
    '''Waits for input from the user. Once an input is recieved, it creates
    a message to send to the server'''
    while True:
        message = input()
        if message == "end":
            sendingSocket.close()
            recievingSocket.close()
            sys.exit()
        currentTime = datetime.datetime.now().strftime("%m-%d-%Y | %H:%M")
        message = '{0} - {1}: {2}' .format(currentTime, name, message)
        sendingSocket.sendto(message.encode('utf-8'), (ServerIP, sendingPort))


def reciever():
    '''Waits for any incoming message from the server'''
    while True:
        data, addr = recievingSocket.recvfrom(4096)
        data = data.decode('utf-8')

        print( data)


def main():
    initialisation()

    t1 = Thread(target=sender, args=())
    t2 = Thread(target=reciever, args =())
    t1.daemon = True
    t2.daemon = True
    t1.start()
    t2.start()
    while True:
        time.sleep(60)



if __name__ == '__main__':

    main()