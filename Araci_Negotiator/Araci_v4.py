import threading
import queue
import socket
import time
import uuid
import json
import sys

sys.path.insert(0, '/home/yasemin/PycharmProjects/dagitik_home_group4-master/dagitik_home_group4')
import QT5_onyuz.dagitik_proje_main

from PyQt5 import QtWidgets, QtGui, QtCore
from Araci_Negotiator import Araci_with_2_threads, Araci_with_2_threads_Logger
from QT5_onyuz.dagitik_proje_ui import Ui_MainWindow
import threading
my_blog_list = []



class ProjectUi(QtWidgets.QMainWindow):
    def __init__(self,logQueue):
        self.logQueue=logQueue

        self.qt_app = QtWidgets.QApplication(sys.argv)
        QtWidgets.QWidget.__init__(self, None)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # list1 =[]
        self.ui.pushButton.pressed.connect(self.connect)
        self.ui.pushButton.pressed.connect(self.get_host_with_port)
        self.ui.pushButton.pressed.connect(self.change_profile_name)
        self.ui.pushButton.pressed.connect(self.disable_button)
        self.ui.pushButton_2.pressed.connect(self.logout_button)
        self.ui.pushButton_7.pressed.connect(self.subscribe_button)
        self.ui.pushButton_3.pressed.connect(self.unsubscribe_button)
        self.ui.pushButton_4.pressed.connect(self.unblock_button)
        self.ui.pushButton_6.pressed.connect(self.block_button)
        self.ui.pushButton_9.pressed.connect(self.send_message_button)
        self.ui.pushButton_5.pressed.connect(self.share_twit_button)

        #self.list =QtWidgets.QListWidget(self)

    def connect(self):
        self.get_host_with_port()
        pass


    def refresh_feed_button(self):
        # takip edilen kişilerin serverlarına istek atarak twitleri yeniler
        pass

    def send_message_button(self):
        # Send message to followed içine yazılan text yalnızca
        # followers içinde check edilen kişilere gönderilecektir
        pass

    def block_button(self):
        # Followers içindeki kullanıcılardan check edilenleri engelleyecektir.
        pass

    def unblock_button(self):
        # Blocked içindeki kullanıcılardan check edilenlerin engellerini kaldıracaktır.
        pass

    def unsubscribe_button(self):
        # Followed içindeki kullanıcılardan check edilenleri takipten çıkacaktır.
        pass

    def subscribe_button(self):
        # Suggested users içindeki kullanıcılardan check edilenleri takip edecektir.
        pass

    def logout_button(self):
        # logout ui kapatma olarak tasarlanmıştır. ileride connection close olarak değiştirilebilir
        self.close()

    def disable_button(self):
        self.ui.pushButton.setDisabled(True)

    def get_host_with_port(self):
        # ip ve port alma işlemi
        self.ip = self.ui.lineEdit.text()
        self.port = self.ui.lineEdit_2.text()
        name = self.ui.lineEdit_3.text()

        request="UINFO"
        myClient = ClientThread("Client Thread", self.ip, self.port, request, self.logQueue)
        response = myClient.control()

        self.ui.listWidget.addItem("XXX"+response+"XXX")

        #self.ui.plainTextEdit_4.setPlainText(i)

        # for i in range(10):
        #    self.ui.listWidget.addItem('Item %s' %(i+1))

        #item = QtGui.QListWidgetItem()
        # item = QtWidgets.QListWidgetItem0
        # item.setText(QtGui.QGuiApplication.translate("Dialog",'x',None,))
        # item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        # item.setCheckState(QtCore.Qt.Unchecked)
        # self.listWidget.addItem(item)

    def change_profile_name(self):
        # kullanıcı adını bağlandığında otomatik olarak değiştirme

        # username =  name parametresi çekilecek
        # username= self.ui.plainTextEdit.toPlainText()
        # self.ui.label_2.setText(username)
        pass

    def share_twit_button(self):
        text = self.ui.plainTextEdit_4.toPlainText()
        request=text.strip()
        myClient = ClientThread("Client Thread", self.ip, self.port, request, self.logQueue)
        response = myClient.control()

        self.ui.listWidget.addItem("XXX"+response+"XXX")

        pass
        '''
        # share butonu ile my blog içerisine twit paylaşımı burası degisecek
        text = self.ui.plainTextEdit_4.toPlainText()
        if len(my_blog_list)==0:
            notification = 'Henüz blog yazılmadı.'
            my_blog_list.append(notification)
            self.ui.listWidget_6.addItems(my_blog_list)
        else:
            my_blog_list.append(text)
            self.ui.listWidget_6.addItems(my_blog_list)
            # twit_list=[]
            # twit1=self.ui.plainTextEdit_4.toPlainText()
            # twit_list.append(twit1)
            # self.ui.listWidget_6.addItems(twit_list) 
        '''

    def suggest_user(self, number_of_suggest, userlist):
        # sayıya göre kullanıcı öneri listesini gösterme

        # self.number_of_suggest = number_of_suggest
        # self.userlist = userlist
        # if userlist is None:
        #    error_notification = 'Baglananan kullanıcı bulunmamaktadır.'
        #    self.ui.listWidget_6.addItems(error_notification)
        pass

    def run(self):
        self.show()
        self.qt_app.exec_()


THREADNUM = 5
CONNECT_POINT_LIST = []  # list array of [ip,port,type,time]
SERVER_PORT = 12351
SERVER_PORT2 = 12352
# SERVER_HOST = socket.gethostbyname(socket.gethostname())
SERVER_HOST = "127.0.0.1"
TYPE = "NEGOTIATOR"

NUMBER_OF_USERLIST = 5
NAME = "MUSTAFA"

serverQueue = queue.Queue()
clientQueue = queue.Queue()

# uuid.NAMESPACE_DNS.hex # dagdelenin metodu(MAC E göre)


userInfoDict = dict()
with open('data.json', 'r') as fp:
    userInfoDict = json.load(fp)
myUUID = uuid.uuid4()
print("my UUID = " + str(myUUID))


# tmpUUID="yasemin"
# userInfoDict[tmpUUID]=["yadress", "yPort", "yNanme", "yNEGOTIATOR"]
# tmpUUID="orhan"
# userInfoDict[tmpUUID]=["oadress", "oPort", "oNanme", "oNEGOTIATOR"]
# tmpUUID="a"
# userInfoDict[tmpUUID]=["4", "4", "4", "4"]


class ArayuzThread(threading.Thread):
    def __init__(self, threadname, logQueue):
        threading.Thread.__init__(self)
        self.threadName = threadname
        self.logQueue = logQueue

    def run(self):
        app = ProjectUi(self.logQueue)
        app.run()


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
        file.write(str(time.ctime()) + "\t\t - " + self.threadName + " starting.\n")
        while not self.exitFlag:
            if not self.logQueue.empty():
                log = self.logQueue.get()
                if log == "QUITT":
                    self.exitFlag = True
                    file.write(str(time.ctime()) + "\t\t - " + "Logger thread : OUITT received." + "\n")
                else:
                    file.write(str(time.ctime()) + "\t\t - " + str(log) + "\n")
        file.write(str(time.ctime()) + "\t\t - " + self.name + "exiting." + "\n")
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

        elif prot == "UINFO":  # YENI KULLANICI İSTEĞİ /KULLANICI BAĞLANTI KONTROLU
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
                        with open('data.json', 'w') as fp:
                            json.dump(userInfoDict, fp)
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

    arayUz = ArayuzThread("Arayüz Thread", logQueue)
    arayUz.start()

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
