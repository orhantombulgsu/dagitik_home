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

STATUS = 0


THREADNUM = 5
CONNECT_POINT_LIST = []  # list array of [ip,port,type,time]
SERVER_PORT  = 12346
SERVER_PORT2 = 12345
# SERVER_HOST = socket.gethostbyname(socket.gethostname())
SERVER_HOST = "127.0.0.1"
TYPE = "NEGOTIATOR"

NUMBER_OF_USERLIST = 5
NAME = "MUSTAFA"

serverQueue = queue.Queue()
clientQueue = queue.Queue()

# uuid.NAMESPACE_DNS.hex # dagdelenin metodu(MAC E göre)


userInfoDict = dict()
try:
    with open('data.json', 'r') as fp:
        userInfoDict = json.load(fp)
except FileNotFoundError:
    with open('data.json', 'w') as fp:
        json.dump(userInfoDict, fp)

myUUID = uuid.uuid4()
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
            # print("UINFODAYIM= " + str(paramIndex))
            if (not paramIndex == -1):
                # print("paramiGectimBenreaderPArserim " + request + " ServerReaderThread")
                paramList = ((request[paramIndex + 1:]).strip()).split('$')
                # print("paramList[0]= "+ str(paramList[0]))
                #with open('data.json', 'r') as fp:
                 #   userInfoDict = json.load(fp)

                if paramList[0] in userInfoDict.keys():
                    response = "CHKED"
                # userInfoList[paramList[0]]=list(paramList[1],paramList[2],paramList[3],paramList[4])
                else:  # BEKLE AZ SEN
                    UUIDtoCheck = paramList[0]
                    # clientQueue.put("CHECK")
                    myClient = ClientThread("Client Thread", paramList[1], int(paramList[2]), "CHECK", self.logQueue)
                    response = myClient.control()
                    # print('RESPONSE:' + response)
                    # print('UUID:' + UUIDtoCheck)
                    if str(response[6:]) == str(UUIDtoCheck):
                        msg = "CONOK"
                        STATUS=1
                        #with open('data.json', 'r') as fp:
                         #   userInfoDict = json.load(fp)

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
            # paramIndex=request.find(":")
            # if(not paramIndex == -1):
            #     nbUser=( request[paramIndex+1:] ).strip()
            i = 0
            paramList = ""
            #with open('data.json', 'r') as fp:
             #   userInfoDict = json.load(fp)

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



        ##BURDAN ITIBAREN YAYINCI ICIN OLANLAR
        elif prot == "PBKEY":  # public_key paylasimi
            if (STATUS == 0):
                response = "CFAIL"
            else:
                paramIndex = request.find(":")
                # print("UINFODAYIM= " + str(paramIndex))
                if (not paramIndex == -1):
                    # print("paramiGectimBenreaderPArserim " + request + " ServerReaderThread")
                    paramList = ((request[paramIndex + 1:]).strip()).split('$')
                    msgToSign=paramList[0]
                    hash = SHA256.new(msgToSign.encode()).digest()
                    print(hash)
                    signature = my_private_key.sign(hash, '')
                    msgToSend = "MYPUB:" + str( (my_public_key.exportKey()).decode() ) + '$' + str(signature)
                    pkstring = my_public_key.exportKey()
                    #pkstring = my_public_key
                    print(pkstring)
                    ####msgToSend = "MYPUB:".encode() + pkstring
                    #msgToSend = "MYPUB:" + str(pkstring) + '$' + str(signature)
                    #print("MYPUBBBB  "+msgToSend)
                    #myClient = ClientThread("Client Thread", SERVER_HOST, int(SERVER_PORT), msgToSend, self.logQueue)
                    #response = myClient.control()
                    self.mySocket.send(msgToSend.encode())
                    #myClient = ClientThread("Client Thread", SERVER_HOST, int(SERVER_PORT), "MYPUB", self.logQueue)
                    #response = myClient.publicKey_control()

                    if response[:5] == "PUBOK":
                        print("PUBOK GELDİİ")
                    elif response[:5] =="PUBER":
                        print("PUBER GELDİİ")
                    response=""

                else:
                    response = "ERROR"




        # elif prot == "SIGNT":  # public_key kontrolu
        #     if (STATUS == 0):
        #         response = "CFAIL"
        #     else:
        #         text_sign = request[7:]
        #         hash = SHA256.new(text_sign.encode()).digest()
        #         signature = private_key.sign(hash, '')
        #         response = "SIGND " + str(signature)

        # elif prot == "MYPUB":  # karisdan pk geldi ama string bunu rsa objesine cevirmeyi yapamadim.
        #     pub = request[7:]
        #     # pk = RSA.generate(2048, pub)
        #     print("PKKKKKK" + pub)
        #     response = "SIGNT " + "abc"
        #
        # elif prot == "SIGND":  # bu mesaj geldiginde yukaridaki gelen public key ile acmak gerekiyor yapamadim.
        #     print("SIGND geldiiiiiiiiiiiiiiiiiii\n")
        #     if (STATUS == 0):
        #         response = "CFAIL"
        #     else:
        #         text_sign = request[7:]
        #         hash = SHA256.new(text_sign.encode()).digest()
        #         if (public_key.verify(hash, request[7:]) == True):
        #             response = "PUBOK"
        #         else:
        #             response = "PUBER"
        #
        # elif prot == "PUBOK":
        #     if (STATUS == 0):
        #         response = "CFAIL"
        #     else:
        #         response = ""
        #
        # elif prot == "PUBER":
        #     if (STATUS == 0):
        #         response = "CFAIL"
        #     else:
        #         response = ""
        #
        #
        #

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
        # print(s.recv(1024).decode())  # blocking'dir
        #print("ClientThread:GönderilenMesaj=" + textToSend)
        mySocket.send((textToSend.strip()).encode())
        response = ((mySocket.recv(1024)).decode()).strip()
        print(type(response))
        #print("ClientThread:AlinanMesaj=" + response)
        mySocket.close()  # Close the socket when done


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
            #is_verified = key.verify(hash,(pub_sifrelimesaj[1]).encode())
            #with open('data.json', 'r') as fp:
             #   userInfoDictt = json.load(fp)
            if(is_verified == True):
                for k in userInfoDict.keys():
                    print("KKKKKKK")
                    print((userInfoDict[k])[0])
                    if (userInfoDict[k])[0]==self.hostToConnect and (userInfoDict[k])[1]==self.portToConnect:
                        print("KEYI ATAMAM LAZIM")
                        (userInfoDict[k])[4] = str(pubkey.exportKey())
                        with open('data.json', 'w') as fp:
                            json.dump(userInfoDict, fp)
                response = "PUBOK"
            else:
                response = "PUBER"
            #pubkey = key.publickey()
            #print("PUBLIIICCC "+key)


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
