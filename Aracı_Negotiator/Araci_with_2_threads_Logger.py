import threading
import queue
import socket
import time
import uuid
import QT5_önyüz.dagitik_proje_main

THREADNUM = 5
CONNECT_POINT_LIST = []  # list array of [ip,port,type,time]
SERVER_PORT = 12343
SERVER_PORT2 = 12344
# SERVER_HOST = socket.gethostbyname(socket.gethostname())
SERVER_HOST = "127.0.0.1"
TYPE = "NEGOTIATOR"

NUMBER_OF_USERLIST = 5
NAME = "MUSTAFA"

serverQueue = queue.Queue()
clientQueue = queue.Queue()

# uuid.NAMESPACE_DNS.hex # dagdelenin metodu(MAC E göre)


userInfoDict = dict()
myUUID = uuid.uuid4()
print("my UUID = " + str(myUUID))
tmpUUID = "yasemin"
userInfoDict[tmpUUID] = ["yadress", "yPort", "yNanme", "yNEGOTIATOR"]
tmpUUID = "orhan"
userInfoDict[tmpUUID] = ["oadress", "oPort", "oNanme", "oNEGOTIATOR"]


class arayüzthread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.Arayüz = QT5_önyüz.dagitik_proje_main.main()
    def run(self):
        pass


# loglama işlemini yapacak thread tanımlanıyor.
class loggerThread(threading.Thread):
    def __init__(self, threadName, logFilePath, logQueue, exitFlag):
        threading.Thread.__init__(self)
        self.threadName = threadName
        self.logQueue = logQueue
        self.logFilePath = logFilePath
        self.exitFlag = exitFlag

    def run(self):
        file = open(self.logFilePath, 'a')
        file.write(str(time.ctime()) + " - " + self.threadName + " starting.\n")
        while not self.exitFlag:
            if not self.logQueue.empty():
                log = self.logQueue.get()
                if log == "QUITT":
                    self.exitFlag = True
                    file.write(str(time.ctime()) + " - " + "Logger thread : OUITT received." + "\n")
                else:
                    file.write(str(time.ctime()) + " - " + str(log) + "\n")
        file.write(str(time.ctime()) + " - " + self.name + "exiting." + "\n")
        file.close()


class ServerThread(threading.Thread):
    def __init__(self, threadName, mySocket, myHostname, myPort, myName, myType, logQueue, exitFlag):
        threading.Thread.__init__(self)
        self.threadName = threadName
        self.mySocket = mySocket
        self.myHostname = myHostname
        self.myPort = myPort
        self.myName = myName
        self.myType = myType
        self.logQueue = logQueue
        self.exitFlag = exitFlag

    def run(self):
        log = "Server thread starting."
        self.logQueue.put(time.ctime() + "\t\t - " + log)
        while True:
            msgReiceved = ((self.mySocket.recv(1024)).decode()).strip()
            if len(msgReiceved) > 1:
                msgToSend = ""
                print("ServerReaderThread " + msgReiceved + " ServerReaderThread")
                log = "Server thread received a message : " + msgReiceved
                self.logQueue.put(time.ctime() + "\t\t - " + log)
                msgToSend = str(self.readerParser(msgReiceved))
                if len(msgToSend) >= 5:
                    self.mySocket.send((msgToSend).encode())
                    log = "Server thread sent a message : " + msgToSend
                    self.logQueue.put(time.ctime() + "\t\t - " + log)

    def readerParser(self, request):
        prot = request[:5]
        response = ""

        print("ReaderParser " + request + " ReaderParser")
        if prot == "HELLO":
            response = "HELLO"

        elif prot == "UINFO":  # YENI KULLANICI İSTEĞİ /KULLANICI BAĞLANTI KONTROLÜ
            paramIndex = request.find(":")
            print("UINFODAYIM= " + str(paramIndex))
            if (not paramIndex == -1):
                print("paramiGectimBenreaderPArserim " + request + " ServerReaderThread")
                paramList = ((request[paramIndex + 1:]).strip()).split('$')
                # print("paramList[0]= "+ str(paramList[0]))
                if paramList[0] in userInfoDict.keys():
                    response = "CHKED"
                # userInfoList[paramList[0]]=list(paramList[1],paramList[2],paramList[3],paramList[4])
                else:  # BEKLE AZ SEN
                    UUIDtoCheck = paramList[0]
                    # clientQueue.put("CHECK")
                    myClient = ClientThread("Client Thread", paramList[1], int(paramList[2]), "CHECK", self.logQueue)
                    response = myClient.control()
                    print('RESPONSE:' + response)
                    print('UUID:' + UUIDtoCheck)
                    if str(response[6:]) == str(UUIDtoCheck):
                        msg = "CONOK"
                        userInfoDict[paramList[0]] = [paramList[1], paramList[2], paramList[3], paramList[4]]
                    else:
                        msg = "CONER"

                    self.mySocket.send(((msg).strip()).encode())
                    log = "Server thread : " + "UUIDs checked.   " + msg
                    self.logQueue.put(time.ctime() + "\t\t - " + log)
                    msgReiceved = ((self.mySocket.recv(1024)).decode()).strip()
                    if len(msgReiceved) > 1:
                        pass


            else:
                response = "ERROR"


        elif prot == "CHECK":  # UUID KONTROLÜ
            response = "MUUID" + ":" + str(myUUID)

        elif prot == "CONOK":  # INF :UUID TUTARLI
            response = "HELLO"

        elif prot == "CONER":  # INF: UUID FARKLI
            response = "BYBYE"

        elif prot == "LSUSR":  # KULLANICI LISTE PAYLASIMI
            # paramIndex=request.find(":")
            # if(not paramIndex == -1):
            #     nbUser=( request[paramIndex+1:] ).strip()
            i = 0
            paramList = ""
            for key in userInfoDict.keys():
                if i < NUMBER_OF_USERLIST:
                    param = key + "," + userInfoDict.get(key)[0] + "," + userInfoDict.get(key)[1] + "," + \
                            userInfoDict.get(key)[2] + "," + userInfoDict.get(key)[3]
                    # print("PARAMMMMMMM"+param)
                    paramList += param + "$"
                else:
                    break
                i += 1
            paramList = paramList[:-1]
            response = "LSUOK" + ":" + paramList
        elif prot == "QUITT":
            response = "EXITT"
            exitFlag = True
            self.logQueue.put("QUITT")

        else:
            response = "ERROR"
        log = "Server thread : " + response
        self.logQueue.put(time.ctime() + "\t\t - " + log)
        return response


class ClientThread(threading.Thread):
    def __init__(self, threadName, hostToConnect, portToConnect, cmnd, logQueue):
        threading.Thread.__init__(self)
        self.threadName = threadName
        self.hostToConnect = hostToConnect
        self.portToConnect = portToConnect
        self.cmnd = cmnd
        self.logQueue = logQueue

    def run(self):
        pass

    def control(self):
        log = self.threadName + " : " + "is controlling."
        self.logQueue.put(time.ctime() + "\t\t - " + log)
        mySocket = socket.socket()  # Create a socket object
        # host = "192.168.1.107"  # Connection point (localhost)
        host = self.hostToConnect  # Connection point (localhost)
        # port = SERVER_PORT  # Reserve a port for your service.
        port = self.portToConnect  # Reserve a port for your service.

        mySocket.connect((host, port))

        prot = self.cmnd[:5]
        if prot == "UINFO":
            paramList = str(myUUID) + "$" + SERVER_HOST + "$" + str(SERVER_PORT) + "$" + NAME + "$" + TYPE
            textToSend = prot + ":" + paramList
        else:
            textToSend = self.cmnd

        log = self.threadName + " : " + "sending a message : " + textToSend
        self.logQueue.put(time.ctime() + "\t\t - " + log)
        # print(s.recv(1024).decode())  # blocking'dir
        mySocket.send((textToSend.strip()).encode())
        response = ((mySocket.recv(1024)).decode()).strip()
        mySocket.close()  # Close the socket when done
        if (response[:5] == "LSUOK"):
            pass

        if len(response) > 1:
            print("ClientThread " + response + " ClientThread")
            log = self.threadName + " : " + "response is " + response
            self.logQueue.put(time.ctime() + "\t\t - " + log)
            return response
        log = self.threadName + " : " + "response is " + ""
        self.logQueue.put(time.ctime() + "\t\t - " + log)
        return ""


class UserInputThread(threading.Thread):
    def __init__(self, threadname, logQueue):
        threading.Thread.__init__(self)
        self.threadName = threadname
        self.logQueue = logQueue

    def run(self):
        log = self.threadName + " : " + "is starting."
        self.logQueue.put(time.ctime() + "\t\t - " + log)
        while True:
            request = input("Enter your request > ")
            log = self.threadName + " : " + "Input request is " + request
            self.logQueue.put(time.ctime() + "\t\t - " + log)
            myClient = ClientThread("Client Thread", SERVER_HOST, SERVER_PORT2, request, self.logQueue)
            response = myClient.control()


def main():
    threads = []
    # ana soket oluşturuluyor ve hangi iplerden bağlantı kabul edileceği, port numarası bilgileri giriliyor..
    mySocket = socket.socket()  # Create a socket object
    host = "0.0.0.0"  # Accesible by all of the network
    port = SERVER_PORT
    mySocket.bind((host, port))  # Bind to the port

    mySocket.listen(5)  # Now wait for client connection,
    # with 5 queued connections at most

    logQueue = queue.Queue()
    exitFlag = False

    Logger = loggerThread("Logger", "log.txt", logQueue, exitFlag)
    Logger.start()

    userInputThread = UserInputThread("User Input Thread", logQueue)
    userInputThread.start()

    arayüz = arayüzthread()

    arayüz.start()
    # for i in range(2):
    while True:
        try:
            log = "Waiting for connection from any client via port number " + str(port)
            logQueue.put(time.ctime() + "\t\t - " + log)
            print("Waiting for connection from any client via port number ", port)
            c, addr = mySocket.accept()  # Establish connection with client. #blocking fonksiyon#c=soket,addr =adress of client
            log = "Got connection from " + str(addr)
            logQueue.put(time.ctime() + "\t\t - " + log)
            print('Got connection from', addr)
            serverThread = ServerThread("Server Thread", c, myUUID, SERVER_HOST, SERVER_PORT, TYPE, logQueue, exitFlag)
            serverThread.start()
            threads.append(serverThread)


        except KeyboardInterrupt:
            break

    #    clientThread = ClientThread("Client Thread")
    #    clientThread.start()
    #  threads.append(clientThread)

    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
