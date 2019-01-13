import threading
import queue
import socket
import time
import uuid
import json
# import sys

#sys.path.insert(0, '/home/mustafa/PycharmProjects/dagitik_home_group4')
#import QT5_onyuz.dagitik_proje_main

from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA256

random_generator = Random.new().read
f_priv = open('id_rsa','w+')
f_pub = open('id_rsa.pub','w+')

if(f_priv and f_pub):
    my_private_key = f_priv.read()
    my_public_key = f_pub.read()
    if(my_private_key == ""):
        new_key = RSA.generate(1024, randfunc=random_generator)
        my_public_key = new_key.publickey()
        f_pub.write(str(my_public_key.exportKey().decode()))
        print(my_public_key.exportKey())
        my_private_key = new_key
        f_priv.write(str(my_private_key.exportKey().decode()))
        #print(new_key.exportKey())

f_priv.close()
f_pub.close()

my_blog_list = []
my_mainpage = []

# my_followed_list=[]
# my_followers_list = []
# my_blacklist = []
# my_inbox_list = []

BLOG = 0


STATUS = 0


THREADNUM = 5
CONNECT_POINT_LIST = []  # list array of [ip,port,type,time]
SERVER_PORT  = 12345
SERVER_PORT2 = 12341
# SERVER_HOST = socket.gethostbyname(socket.gethostname())
#SERVER_HOST = "127.0.0.1"
#TYPE = "NEGOTIATOR"
SERVER_HOST="172.20.10.9"
SERVER_HOST_2="172.20.10.10"
TYPE="YAYINCI"

NUMBER_OF_USERLIST = 5
NAME = "YASEMIN"

serverQueue = queue.Queue()
clientQueue = queue.Queue()

userInfoDict = dict()

try:
    with open('data.json', 'r') as fp:
        userInfoDict = json.load(fp)
except FileNotFoundError:
    with open('data.json', 'w') as fp:
        json.dump(userInfoDict, fp)

myUUID = uuid.uuid1()
print("my UUID = " + str(myUUID))


# tmpUUID="yasemin"
# userInfoDict[tmpUUID]=["yadress", "yPort", "yNanme", "yNEGOTIATOR",None]
# tmpUUID="orhan"
# userInfoDict[tmpUUID]=["oadress", "oPort", "oNanme", "oNEGOTIATOR",None]
# tmpUUID="a"
# userInfoDict[tmpUUID]=["4", "4", "4", "4",None]
# with open('data.json', 'w') as fp:
#     json.dump(userInfoDict, fp)


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
                print("ServerThread:AlinanMesaj=" + msgReiceved)
                log = "Server thread received a message : " + msgReiceved
                self.logQueue.put(time.ctime() + "\t\t - " + log)
                msgToSend = str(self.readerParser(msgReiceved))
                if len(msgToSend) >= 5:
                    print("ServerThread:GönderilenMesaj=" + msgToSend)
                    self.mySocket.send((msgToSend).encode())
                    log = "Server thread sent a message : " + msgToSend
                    self.logQueue.put(time.ctime() + "\t\t - " + log)

    def readerParser(self, request):
        prot = request[:5]
        response = ""
        global STATUS
        global userInfoDict

        if prot == "HELLO":
            response = "HELLO"

        elif prot == "UINFO":  # YENI KULLANICI İSTEĞİ /KULLANICI BAĞLANTI KONTROLU
            paramIndex = request.find(":")
            if (not paramIndex == -1):
                paramList = ((request[paramIndex + 1:]).strip()).split('$')

                if paramList[0] in userInfoDict.keys():
                    response = "CHKED"

                else:  # Kontrol için bekletme
                    UUIDtoCheck = paramList[0]
                    # clientQueue.put("CHECK")
                    myClient = ClientThread("Client Thread", paramList[1], int(paramList[2]), "CHECK", self.logQueue)
                    response = myClient.control()
                    # print('RESPONSE:' + response)
                    # print('UUID:' + UUIDtoCheck)
                    if str(response[6:]) == str(UUIDtoCheck):
                        msg = "CONOK"
                        STATUS=1

                        userInfoDict[paramList[0]] = [paramList[1], paramList[2], paramList[3], paramList[4],None]

                        with open('data.json', 'w') as fp:
                            json.dump(userInfoDict, fp)
                    else:
                        msg = "CONER"

                    print("ServerThread:GönderilenMesaj=" + msg)
                    self.mySocket.send(((msg).strip()).encode())
                    log = "Server thread : " + "UUIDs checked.   " + msg
                    self.logQueue.put(time.ctime() + "\t\t - " + log)
                    msgReiceved = ((self.mySocket.recv(1024)).decode()).strip()
                    if len(msgReiceved) > 1:
                        print("ServerThread:AlinanMesaj=" + msgReiceved)
                        pass


            else:
                response = "ERROR"


        elif prot == "CHECK":  # UUID KONTROLU
            response = "MUUID" + ":" + str(myUUID)

        elif prot == "CONOK":  # INF :UUID TUTARLI
            response = "HELLO"

        elif prot == "CONER":  # INF: UUID FARKLI
            response = "BYBYE"

        elif prot == "LSUSR":  # KULLANICI LISTE PAYLASIMI
            i = 0
            paramList = ""

            for key in userInfoDict.keys():
                if i < NUMBER_OF_USERLIST:
                    param = key + "," + userInfoDict.get(key)[0] + "," + userInfoDict.get(key)[1] + "," + \
                            userInfoDict.get(key)[2] + "," + userInfoDict.get(key)[3]
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



        ##BURADAN ITIBAREN YAYINCI ICIN OLANLAR
        elif prot == "PBKEY":  # public_key paylasimi
            if (STATUS == 0):
                response = "CFAIL"
            else:
                paramIndex = request.find(":")
                if (not paramIndex == -1):
                    paramList = ((request[paramIndex + 1:]).strip()).split('$')
                    msgToSign=paramList[0]
                    hash = SHA256.new(msgToSign.encode()).digest()
                    print(hash)

                    signature = my_private_key.sign(hash, '')
                    msgToSend = "MYPUB:" + str( (my_public_key.exportKey()).decode() ) + '$' + str(signature)

                    pkstring = my_public_key.exportKey()
                    print(pkstring)

                    self.mySocket.send(msgToSend.encode())

                    if response[:5] == "PUBOK":
                        print("PUBOK GELDİİ")
                    elif response[:5] =="PUBER":
                        print("PUBER GELDİİ")
                    response=""

                else:
                    response = "ERROR"


        ##BURADAN ITIBAREN SIFRELILER


        # elif prot == "SNDMB":
        #     paramIndex = request.find(":")
        #
        #     if (not paramIndex == -1):
        #         paramList = ((request[paramIndex + 1:]).strip()).split('$')
        #         recv_uuid = paramList[0]
        #         if(not recv_uuid in userInfoDict.keys):
        #             response = "CFAIL"
        #         else:
        #             if recv_uuid in my_blacklist:
        #                 response = "BLCKD"
        #             else:
        #                 numberOfBlogs = int(paramList[1])
        #                 response =  "MYMBS:"+my_blog_list[0:numberOfBlogs]
        #
        #
        # elif prot == "SBLOG":
        #     paramIndex = request.find(":")
        #
        #     if (not paramIndex == -1):
        #         paramList = ((request[paramIndex + 1:]).strip()).split('$')
        #         recv_uuid = uuid.UUID(paramList[0])
        #         if(not recv_uuid in userInfoDict.keys):
        #             response = "CFAIL"
        #         else:
        #             if recv_uuid in my_blacklist:
        #                 response = "BLCKD"
        #             else:
        #                 my_mainpage.append(paramList[1])
        #                 print("MAINPAGE: ")
        #                 print(my_mainpage)
        #                 response = "BLGOK"
        #
        # elif prot == "BLOCK":
        #     paramIndex = request.find(":")
        #
        #     if (not paramIndex == -1):
        #         paramList = ((request[paramIndex + 1:]).strip()).split('$')
        #         recv_uuid = uuid.UUID(paramList[0])
        #         if(not recv_uuid in userInfoDict.keys):
        #             response = "CFAIL"
        #         else:
        #             response = "BLCOK"
        #
        # elif prot == "UNBLC":
        #     paramIndex = request.find(":")
        #
        #     if (not paramIndex == -1):
        #         paramList = ((request[paramIndex + 1:]).strip()).split('$')
        #         recv_uuid = uuid.UUID(paramList[0])
        #         if(not recv_uuid in userInfoDict.keys):
        #             response = "CFAIL"
        #         else:
        #             response = "UNBOK"
        #
        #
        # elif prot == "SUBSC":
        #     recv_uuid = uuid.UUID(request[6:])
        #     if(not recv_uuid in userInfoDict.keys):
        #         response = "CFAIL"
        #     else:
        #         if recv_uuid in my_blacklist:
        #             response = "BLCKD"
        #         else:
        #             response = "SUBOK"
        #             my_followers_list.append(recv_uuid)
        #
        # elif prot == "UNSUB":
        #     recv_uuid = uuid.UUID(request[6:])
        #     if(not recv_uuid in userInfoDict.keys):
        #         response = "CFAIL"
        #     else:
        #         response = "USBOK"
        #         my_followers_list.remove(recv_uuid)

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
        global BLOG
        global userInfoDict
        log = self.threadName + " : " + "is controlling."
        self.logQueue.put(time.ctime() + "\t\t - " + log)
        mySocket = socket.socket()  # Create a socket object
        # host = "192.168.1.107"  # Connection point (localhost)
        host = self.hostToConnect  # Connection point (localhost)
        # port = SERVER_PORT  # Reserve a port for your service.
        port = self.portToConnect  # Reserve a port for your service.

        mySocket.connect((host, int(port)))

        prot = self.cmnd[:5]
        if prot == "UINFO":
            paramList = str(myUUID) + "$" + SERVER_HOST + "$" + str(SERVER_PORT) + "$" + NAME + "$" + TYPE
            textToSend = prot + ":" + paramList
        else:
            textToSend = self.cmnd

        log = self.threadName + " : " + "sending a message : " + textToSend
        self.logQueue.put(time.ctime() + "\t\t - " + log)
        mySocket.send((textToSend.strip()).encode())
        response = ((mySocket.recv(1024)).decode()).strip()
        print(type(response))
        #print("ClientThread:AlinanMesaj=" + response)
        mySocket.close()


        if(response[:5] == "MYPUB"):
            pub_sifrelimesaj=response[6:].strip().split("$")
            print(type(pub_sifrelimesaj[0]))
            print("PKKK = " + pub_sifrelimesaj[0])
            print("sifreli mesaj = " + pub_sifrelimesaj[1])
            pubkey = RSA.importKey((pub_sifrelimesaj[0]).encode())
            hash= SHA256.new("BUNUIMZALA".encode()).digest()
            print(hash)
            print((pub_sifrelimesaj[1]).encode())
            signature = int(pub_sifrelimesaj[1][1:-1].split(",")[0])
            signature = (signature, '')
            is_verified = pubkey.verify(hash,signature)

            if(is_verified == True):
                for k in userInfoDict.keys():
                    print((userInfoDict[k])[0])
                    if (userInfoDict[k])[0]==self.hostToConnect and (userInfoDict[k])[1]==self.portToConnect:
                        #print("KEYI ATAMAM LAZIM")
                        (userInfoDict[k])[4] = str(pubkey.exportKey())
                        with open('data.json', 'w') as fp:
                            json.dump(userInfoDict, fp)
                response = "PUBOK"
            else:
                response = "PUBER"


        #if(response[:5] == "BLGOK"):
         #   BLOG = 1
            #my_mainpage.append(self.cmnd[7:])


        if (response[:5] == "LSUOK"):
            pass

        if len(response) > 1:
            # print("ClientThread " + response + " ClientThread")
            log = self.threadName + " : " + "response is " + response
            self.logQueue.put(time.ctime() + "\t\t - " + log)
            return response
        log = self.threadName + " : " + "response is " + ""
        self.logQueue.put(time.ctime() + "\t\t - " + log)
        return ""

class UserInputThread(threading.Thread): #Ara yuz yazilmadan once komut satiri ile deneme yapmak icin yazilmistir.
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
            myClient = ClientThread("Client Thread", SERVER_HOST, SERVER_PORT, request, self.logQueue)
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

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()
