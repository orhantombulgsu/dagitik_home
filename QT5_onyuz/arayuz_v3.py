import sys
sys.path.insert(0, '/home/yasemin/PycharmProjects/dagitik_home_group4-master/dagitik_home_group4')

from PyQt5 import QtWidgets, QtGui, QtCore
from Yayıncı_Blogger import Yayinci_v3 as yay
from QT5_onyuz.dagitik_proje_ui import Ui_MainWindow
my_blog_list = []

import threading
import queue
import socket
import time




class ProjectUi(QtWidgets.QMainWindow):
    def __init__(self,logQueue):
        self.logQueue=logQueue

        self.qt_app = QtWidgets.QApplication(sys.argv)
        QtWidgets.QWidget.__init__(self, None)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # list1 =[]
        self.ui.pushButton.pressed.connect(self.connect)
        # self.ui.pushButton.pressed.connect(self.get_host_with_port)
        self.ui.pushButton.pressed.connect(self.change_profile_name)
        # self.ui.pushButton.pressed.connect(self.disable_button)
        self.ui.pushButton_2.pressed.connect(self.logout_button)
        self.ui.pushButton_7.pressed.connect(self.subscribe_button)
        self.ui.pushButton_3.pressed.connect(self.unsubscribe_button)
        self.ui.pushButton_4.pressed.connect(self.unblock_button)
        self.ui.pushButton_6.pressed.connect(self.block_button)
        self.ui.pushButton_9.pressed.connect(self.send_message_button)
        self.ui.pushButton_5.pressed.connect(self.share_twit_button)
        self.initializeIpPort()

        #self.list =QtWidgets.QListWidget(self)

    def initializeIpPort(self):
        self.ui.lineEdit.setText("127.0.0.1")
        self.ui.lineEdit_2.setText("12242")
        self.ui.lineEdit_3.setText("Mustafa")

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
        # self.close()
        request="PBKEY:"+"BUNUIMZALA"
        myClient = yay.ClientThread("Client Thread", self.ip, self.port, request, self.logQueue)
        response = myClient.control()
        self.ui.listWidget.addItem("XXX"+response+"XXX")



    def disable_button(self):
        self.ui.pushButton.setDisabled(True)

    def get_host_with_port(self):
        # ip ve port alma işlemi
        self.ip = self.ui.lineEdit.text()
        self.port = self.ui.lineEdit_2.text()
        name = self.ui.lineEdit_3.text()

        request="UINFO"
        myClient = yay.ClientThread("Client Thread", self.ip, self.port, request, self.logQueue)
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
        username = self.ui.lineEdit_3.text()
        self.ui.label_2.setText(username)

    def share_twit_button(self):
        text = self.ui.plainTextEdit_4.toPlainText()
        request=text.strip()
        myClient = yay.ClientThread("Client Thread", self.ip, self.port, request, self.logQueue)
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


class ArayuzThread(threading.Thread):
    def __init__(self, threadname, logQueue):
        threading.Thread.__init__(self)
        self.threadName = threadname
        self.logQueue = logQueue

    def run(self):
        app = ProjectUi(self.logQueue)
        app.run()




def main():
    threads = []
    # ana soket oluşturuluyor ve hangi iplerden bağlantı kabul edileceği, port numarası bilgileri giriliyor..
    mySocket = socket.socket()  # Create a socket object
    host = "0.0.0.0"  # Accesible by all of the network
    port = yay.SERVER_PORT
    mySocket.bind((host, port))  # Bind to the port

    mySocket.listen(5)  # Now wait for client connection,
    # with 5 queued connections at most

    logQueue = queue.Queue()
    exitFlag = False

    Logger = yay.loggerThread("Logger", "log.txt", logQueue, exitFlag)
    Logger.start()

    userInputThread = yay.UserInputThread("User Input Thread", logQueue)
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
            serverThread = yay.ServerThread("Server Thread", c, yay.myUUID, yay.SERVER_HOST, yay.SERVER_PORT, yay.TYPE, logQueue, exitFlag)
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
