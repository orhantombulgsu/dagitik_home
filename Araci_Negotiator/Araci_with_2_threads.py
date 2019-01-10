import threading
import queue
import socket
import time
import uuid

THREADNUM = 5
CONNECT_POINT_LIST = []  # list array of [ip,port,type,time]
SERVER_PORT =  12352
SERVER_PORT2 = 12351
# SERVER_HOST = socket.gethostbyname(socket.gethostname())
SERVER_HOST = "127.0.0.1"
TYPE = "NEGOTIATOR"

NUMBER_OF_USERLIST = 5
NAME = "MUSTAFA"

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
    def __init__(self, threadName,mySocket,myHostname,myPort,myName,myType):
        threading.Thread.__init__(self)
        self.threadName=threadName
        self.mySocket=mySocket
        self.myHostname=myHostname
        self.myPort=myPort
        self.myName=myName
        self.myType=myType

    def run(self):
        while True:
            msgReiceved = ( (self.mySocket.recv(1024)).decode() ).strip()
            if len(msgReiceved) > 1:
                msgToSend=""
                print("ServerReaderThread "+msgReiceved+" ServerReaderThread")
                msgToSend=str(self.readerParser(msgReiceved)    )
                if len(msgToSend) >= 5:
                    self.mySocket.send( ( msgToSend ).encode() )



    def readerParser(self, request):
        prot=request[:5]
        response=""

        print("ReaderParser " + request + " ReaderParser")
        if prot == "HELLO":
            response="HELLO"

        elif prot == "UINFO": # YENI KULLANICI İSTEĞİ /KULLANICI BAĞLANTI KONTROLÜ
            paramIndex=request.find(":")
            print("UINFODAYIM= "+str(paramIndex))
            if(not paramIndex == -1):
                print("paramiGectimBenreaderPArserim "+request+" ServerReaderThread")
                paramList= ( ( request[paramIndex+1:] ).strip() ).split('$')
                # print("paramList[0]= "+ str(paramList[0]))
                if paramList[0] in userInfoDict.keys():
                    response = "CHKED"
                # userInfoList[paramList[0]]=list(paramList[1],paramList[2],paramList[3],paramList[4])
                else: # BEKLE AZ SEN
                    print("Else in icindeyim")
                    UUIDtoCheck=paramList[0]
                    # clientQueue.put("CHECK")
                    myClient=ClientThread("Client Thread",paramList[1],int(paramList[2]),"CHECK")
                    response=myClient.control()
                    print("Client yaratildii")
                    print('RESPONSE:' + response)
                    print('UUID:' + UUIDtoCheck)
                    if str(response[6:]) == str(UUIDtoCheck):
                        msg="CONOK"
                        userInfoDict[paramList[0]]=[paramList[1], paramList[2], paramList[3], paramList[4]]
                    else:
                        msg="CONER"

                    self.mySocket.send( ( (msg).strip() ).encode() )
                    msgReiceved = ( (self.mySocket.recv(1024)).decode() ).strip()
                    if len(msgReiceved) > 1:
                        pass


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




class ClientThread(threading.Thread):
    def __init__(self, threadName, hostToConnect,portToConnect,cmnd):
        threading.Thread.__init__(self)
        self.threadName=threadName
        self.hostToConnect=hostToConnect
        self.portToConnect=portToConnect
        self.cmnd=cmnd


    def run(self):
        pass
    def control(self):
        mySocket = socket.socket()  # Create a socket object
        # host = "192.168.1.107"  # Connection point (localhost)
        host = self.hostToConnect  # Connection point (localhost)
        # port = SERVER_PORT  # Reserve a port for your service.
        port = self.portToConnect  # Reserve a port for your service.

        mySocket.connect((host, port))


        prot=self.cmnd[:5]
        if prot == "UINFO":
            paramList = str(myUUID) + "$" + SERVER_HOST + "$" + str(SERVER_PORT) + "$" + NAME + "$" + TYPE
            textToSend = prot + ":" + paramList
        else:
            textToSend=self.cmnd

        # print(s.recv(1024).decode())  # blocking'dir
        mySocket.send( (textToSend.strip()).encode() )
        response= ( ( mySocket.recv(1024) ).decode() ).strip()
        mySocket.close()  # Close the socket when done
        if(response[:5]=="LSUOK"):
            pass

        if len(response) > 1:
            print ( "ClientThread " + response + " ClientThread"  )
            return response
        return ""


class UserInputThread(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name=name
    def run(self):
        while True:
            request = input("Enter your request > ")
            myClient=ClientThread("Client Thread",SERVER_HOST,SERVER_PORT2,request)
            response=myClient.control()


def main():
    threads = []
    # ana soket oluşturuluyor ve hangi iplerden bağlantı kabul edileceği, port numarası bilgileri giriliyor..
    mySocket = socket.socket()  # Create a socket object
    host = "0.0.0.0"  # Accesible by all of the network
    port = SERVER_PORT
    mySocket.bind((host, port))  # Bind to the port

    mySocket.listen(5)  # Now wait for client connection,
    # with 5 queued connections at most
    userInputThread = UserInputThread("user Input Thread")
    userInputThread.start()

    # for i in range(2):
    while True:
        try:
            print("Waiting for connection from any client via port number ", port)
            c, addr = mySocket.accept()  # Establish connection with client. #blocking fonksiyon#c=soket,addr =adress of client
            print('Got connection from', addr)
            serverThread = ServerThread("Server Thread",c,myUUID,SERVER_HOST,SERVER_PORT,TYPE)
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
