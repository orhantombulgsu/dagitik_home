import threading
import queue
import socket
import time
import uuid

THREADNUM = 5
CONNECT_POINT_LIST = []  # list array of [ip,port,type,time]
SERVER_PORT = 12391
# SERVER_HOST = socket.gethostbyname(socket.gethostname())
SERVER_HOST = "127.0.0.1"
NUMBER_OF_USERLIST = 5
NAME = "MUSTAFA"
TYPE = "NEGOTIATOR"
print(SERVER_HOST)

serverQueue = queue.Queue()
clientQueue = queue.Queue()
logQueue = queue.Queue()






# uuid.NAMESPACE_DNS.hex # dagdelenin metodu(MAC E göre)








userInfoDict = dict()
myUUID=uuid.uuid4()
print("my UUID = "+str(myUUID))
tmpUUID="yasemin"
userInfoDict[tmpUUID]=["yadress", "yPort", "yNanme", "yNEGOTIATOR"]
tmpUUID="orhan"
userInfoDict[tmpUUID]=["oadress", "oPort", "oNanme", "oNEGOTIATOR"]

UUIDtoCheck=""

#loglama işlemini yapacak thread tanımlanıyor.
class loggerThread(threading.Thread):
    def __init__(self, threadID, name, logFilePath):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.file = open(logFilePath, 'w')
        self.exitCode=False

    def run(self):
        while not self.exitCode:
            if not logQueue.empty():
                self.file.write(logQueue.get()+"\n")
        self.file.close()


class ServerThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name=name


    def run(self):
        # loggerThread oluşturulup çalıştırılıyor.
        myLogConn = loggerThread(1, "Logger_Thread", "logConnections.txt")
        myLogConn.start()

        # ana soket oluşturuluyor ve hangi iplerden bağlantı kabul edileceği, port numarası bilgileri giriliyor..
        mySocket = socket.socket()  # Create a socket object
        host = "0.0.0.0"  # Accesible by all of the network
        port = SERVER_PORT
        mySocket.bind((host, port))  # Bind to the port

        # bağlantıların tutulacağı liste
        connections = []
        i = 1

        mySocket.listen(5)  # Now wait for client connection,
        # with 5 queued connections at most

        # for i in range(2):
        while True:
            try:
                print("Waiting for connection from any client via port number ", port)
                c, addr = mySocket.accept()  # Establish connection with client. #blocking fonksiyon#c=soket,addr =adress of client
                print('Got connection from', addr)
                myReader= ServerReaderThread("Server Reader Thread",c)
                myWriter= ServerWriterThread("Server Writer Thread",c)

                myReader.start()
                myWriter.start()

                myReader.join()
                myWriter.join()

            except KeyboardInterrupt:
                break
        for c in connections:
            c.join()

        # loggerThread' e işini bitir ve çık komutu veriliyor. log dosyası kapatılıyor ve program sonlanıyor.
        myLogConn.exitCode = True
        myLogConn.join()


class ServerWriterThread(threading.Thread):
    def __init__(self, name,soket):
        threading.Thread.__init__(self)
        self.name=name
        self.soket=soket

    def run(self):
        while True:
            if serverQueue.empty():
                msg=serverQueue.get() + "\n"
                print("ServerWriterThread "+msg+" ServerWriterThread")
                self.soket.send(msg.encode())

class ServerReaderThread(threading.Thread):
    def __init__(self, name,soket):
        threading.Thread.__init__(self)
        self.name=name
        self.soket=soket


    def run(self):
        while(True):
            msgReiceved = (self.soket.recv(1024)).decode()
            msgReiceved=msgReiceved.strip()
            if len(msgReiceved) > 1:
                print("ServerReaderThread "+msgReiceved+" ServerReaderThread")
                msgToSend=self.readerParser(msgReiceved)
                serverQueue.put(msgToSend)

    def readerParser(self, request):
        prot=request[:5]
        response=""

        if prot == "HELLO":
            response="HELLO"

        elif prot == "UINFO": # YENI KULLANICI İSTEĞİ /KULLANICI BAĞLANTI KONTROLÜ
            print("ReaderParser " + request + " ServerReaderThread")
            paramIndex=request.find(":")
            # print("paramIndex= "+str(paramIndex))
            if(not paramIndex == -1):
                print("paramiGectimBenreaderPArserim "+request+" ServerReaderThread")
                paramList= ( ( request[paramIndex+1:] ).strip() ).split('$')
                # print("paramList[0]= "+ str(paramList[0]))
                if paramList[0] in userInfoDict.keys():
                    response = "CHKED"
                # userInfoList[paramList[0]]=list(paramList[1],paramList[2],paramList[3],paramList[4])
                else: # BEKLE AZ SEN
                    UUIDtoCheck=paramList[0]
                    # clientQueue.put("CHECK")
                    response="CNTRL"
            else:
                response="ERROR"


        elif prot == "CHECK": # UUID KONTROLÜ
            response="MUUID"+":"+str(myUUID)

        elif prot == "CONOK": # INF :UUID TUTARLI
            response="HELLO"

        elif prot == "CONER": # INF: UUID FARKLI
            response="BYBYE"

        elif prot == "LSUSR": # KULLANICI LISTE PAYLASIMI
            # paramIndex=request.find(":")
            # if(not paramIndex == -1):
            #     nbUser=( request[paramIndex+1:] ).strip()
            i=0
            paramList = ""
            for key in userInfoDict.keys():
                if i<NUMBER_OF_USERLIST:
                    param=key+","+userInfoDict.get(key)[0]+","+userInfoDict.get(key)[1]+","+userInfoDict.get(key)[2]+","+userInfoDict.get(key)[3]
                    # print("PARAMMMMMMM"+param)
                    paramList+=param+"$"
                else:
                    break
                i+= 1
            paramList=paramList[:-1]
            response="LSUOK"+":"+paramList

        else:
            response="ERROR"

        return response


class UserInputThread(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name=name
    def run(self):
        while True:
            request = input("Enter your request > ")
            clientQueue.put(request)


class ClientThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name=name

    def run(self):
        userInputThread = UserInputThread("user Input Thread")
        userInputThread.start()
        while True:
            # while True:
            #     request = input("Enter your request > ")
            #     clientQueue.put(request)
            #     break
            if not clientQueue.empty():
                mySocket = socket.socket()  # Create a socket object
                # host = "192.168.1.107"  # Connection point (localhost)
                host = SERVER_HOST  # Connection point (localhost)
                # port = SERVER_PORT  # Reserve a port for your service.
                port = 12392  # Reserve a port for your service.

                mySocket.connect((host, port))

                # print(s.recv(1024).decode())  # blocking'dir

                myReader= ClientReaderThread("Client Reader Thread",mySocket)
                myWriter= ClientWriterThread("Client Writer Thread",mySocket)

                myReader.start()
                myWriter.start()

                myReader.join()
                myWriter.join()

                mySocket.close()  # Close the socket when done
        userInputThread.join()


class ClientWriterThread(threading.Thread):
    def __init__(self, name,soket):
        threading.Thread.__init__(self)
        self.name=name
        self.soket=soket

    def run(self):
        # while True:
        if not clientQueue.empty():
            request=clientQueue.get()
            prot=request[:5]
            if prot == "HELLO":
                self.soket.send(request.strip().encode())
            elif prot == "UINFO":
                paramList = str(myUUID) + "$" + SERVER_HOST + "$" + str(SERVER_PORT) + "$" + NAME + "$" + TYPE
                textToSend = prot + ":" + paramList
                self.soket.send(textToSend.strip().encode())
            elif prot == "CHECK":
                self.soket.send(request.strip().encode())
            elif prot == "CONOK":
                self.soket.send(request.strip().encode())
            elif prot == "CONER":
                self.soket.send(request.strip().encode())
            elif prot == "LSUSR":
                self.soket.send(request.strip().encode())
            else:
                self.soket.send( ("ERROR").encode() )

class ClientReaderThread(threading.Thread):
    def __init__(self, name,soket):
        threading.Thread.__init__(self)
        self.name=name
        self.soket=soket

    def run(self):
        response= ( ( self.soket.recv(1024) ).decode() ).strip()
        print("ClientReaderThread "+response+" ClientReaderThread")
        prot=response[:5]
        if prot == "CNTRL":
            pass
        elif prot == "CHKED":
            pass
        elif prot == "MUUID":
            paramIndex=response.find(":")
            if( not paramIndex==-1 ):
                tempUUID=( response[paramIndex+1:] ).strip()
                print("BEN ClientReaderThreadİM,şimdi karşılaştırıcam")
                tempUUID=tempUUID.strip()
                print("XXX"+UUIDtoCheck+"XXX")
                print("XXX"+tempUUID+"XXX")
                # UUIDtoCheck=UUIDtoCheck.strip()

                if tempUUID == UUIDtoCheck:
                    print("BEN ClientReaderThreadİM,şimdi karşılaştırdım, OK")
                    # clientQueue.put("CONOK")
                else:
                    print("BEN ClientReaderThreadİM,şimdi karşılaştırdım, ER")
                    # clientQueue.put("CONER")


        elif prot == "HELLO":
            pass
        else:
            pass



def main():
    threads = []

    try:

        serverThread = ServerThread("Server Thread")
        serverThread.start()
        threads.append(serverThread)

        clientThread = ClientThread("Client Thread")
        clientThread.start()
        threads.append(clientThread)

        for t in threads:
            t.join()
    except Exception as ex:
        print(__name__, ex)


if __name__ == '__main__':
    main()