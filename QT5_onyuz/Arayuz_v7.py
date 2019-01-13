import sys
import json

sys.path.insert(0, '/home/yasemin/PycharmProjects/dagitik_home_group4-master/dagitik_home_group4')
#sys.path.insert(0, '/home/mustafa/PycharmProjects/dagitik_home_group4')
#sys.path.insert(0, '/home/admin/dagitik_home_group4')


from PyQt5 import QtWidgets, QtGui, QtCore
from Yayinci_Blogger import Yayinci_v5 as yay
from QT5_onyuz.dagitik_proje_v2_ui import Ui_MainWindow


my_blog_list = []

import threading
import queue
import socket
import time




class ProjectUi(QtWidgets.QMainWindow):
    def __init__(self, logQueue):
        self.logQueue = logQueue

        self.qt_app = QtWidgets.QApplication(sys.argv)
        QtWidgets.QWidget.__init__(self, None)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # list1 =[]
        self.ui.connect_button.pressed.connect(self.connect)
        # self.ui.connect_button.pressed.connect(self.get_host_with_port)
        self.ui.connect_button.pressed.connect(self.change_profile_name)
        # self.ui.connect_button.pressed.connect(self.disable_button)
        self.ui.LogOut_button.pressed.connect(self.logout_button)
        self.ui.Subscribe_button.pressed.connect(self.subscribe_button)
        self.ui.UnSubscribe_button.pressed.connect(self.unsubscribe_button)
        self.ui.UnBlock_button.pressed.connect(self.unblock_button)
        self.ui.Block_button.pressed.connect(self.block_button)
        self.ui.SendMessage_button.pressed.connect(self.send_message_button)
        self.ui.Share_button.pressed.connect(self.share_twit_button)
        self.ui.Pubkey_button.pressed.connect(self.pubkey_button)
        self.ui.users_button.pressed.connect(self.users_button)
        self.initializeIpPort()
        self.initialize_button_conf()
        self.initializeMyBlogsList()
        #self.initializeLists()

    def initializeMyBlogsList(self):
        try:
            f_myBlogs = open('Mb.txt', 'r')
            if f_myBlogs is None:
                print("Error: Can not open f_myBlogs\n")
            else:
                print("Dosya acildi\n")
                for line in f_myBlogs:
                    yay.my_blog_list.append(line)
            f_myBlogs.close()

            for item in yay.my_blog_list:
                self.ui.MyBlogList_field.addItem(item)
        except FileNotFoundError:
            pass

    # def read_from_file(self, filename, fieldName):
    #     try:
    #         with open(filename, 'r') as fp:
    #             retList = json.load(fp)
    #
    #             for item in retList:
    #                 fieldName.addItem(item)
    #         return retList
    #
    #     except FileNotFoundError:
    #         pass
    #
    # def write_to_file(self, filename, list):
    #     try:
    #         with open('data.json', 'w') as fp:
    #             json.dump(list, fp)
    #
    #     except FileNotFoundError:
    #         pass
    #
    # def initializeLists(self):
    #     yay.my_blog_list = self.read_from_file( "MyBlogs.json", self.ui.MyBlogList_field)
    #     yay.my_followed_list = self.read_from_file( "MyFollowed.json", self.ui.Followed_field)
    #     yay.my_followers_list = self.read_from_file( "MyFollowers.json", self.ui.Followers_field)
    #     yay.my_mainpage = self.read_from_file( "MyMainpage.json", self.ui.Feeds_field)
    #     #yay.my_inbox_list = self.read_from_file( "MyInbox.json", self.ui.Inbox_field)
    #     yay.my_blacklist = self.read_from_file( "MyBlacklist.json", self.ui.Blocked_field)

    def initialize_button_conf(self):
        pass
        #fldchbx1 = self.ui.fldchbx1
        #fldchbx2 = self.ui.fldchbx2
        #fldchbx3 = self.ui.fldchbx3
        #fldchbx4 = self.ui.fldchbx4
        #fldchbx5 = self.ui.fldchbx5
        #followed_checkboxlist.append(fldchbx1)
        #followed_checkboxlist.append(fldchbx2)
        #followed_checkboxlist.append(fldchbx3)
        #followed_checkboxlist.append(fldchbx4)
        #followed_checkboxlist.append(fldchbx5)
#
#
        #flwchbx1 = self.ui.flwchbx1
        #flwchbx2 = self.ui.flwchbx2
        #flwchbx3 = self.ui.flwchbx3
        #flwchbx4 = self.ui.flwchbx4
        #flwchbx5 = self.ui.flwchbx5
        #followers_checkboxlist.append(flwchbx1)
        #followers_checkboxlist.append(flwchbx2)
        #followers_checkboxlist.append(flwchbx3)
        #followers_checkboxlist.append(flwchbx4)
        #followers_checkboxlist.append(flwchbx5)
#
        #blkchbx1 = self.ui.blkchbx1
        #blkchbx2 = self.ui.blkchbx2
        #blkchbx3 = self.ui.blkchbx3
        #blkchbx4 = self.ui.blkchbx4
        #blkchbx5 = self.ui.blkchbx5
        #blocked_checkboxlist.append(blkchbx1)
        #blocked_checkboxlist.append(blkchbx2)
        #blocked_checkboxlist.append(blkchbx3)
        #blocked_checkboxlist.append(blkchbx4)
        #blocked_checkboxlist.append(blkchbx5)

    def users_button(self):
        suggest_checkboxlist = []
        usernamelist = []
        request="LSUSR"
        myClient = yay.ClientThread("Client Thread", self.ip, self.port, request, self.logQueue)
        response = myClient.control()
        self.ui.LogLabel_field.setText("XXX"+response+"XXX")
        users = response[6:].split("$")
        i=0;
        userList=dict()
        for u in users:
            print(u)
            x=u.split(",")
            userList[x[0]] = [   x[1],x[2],x[3],x[4], None ]
            suggest_checkboxlist.append(userList[x[0]])
            usernamelist.append(x[3])

        suggest_checkboxlist.append(self.ui.sugchbx1)
        self.ui.sugchbx1.setText(usernamelist[0])
        suggest_checkboxlist.append(self.ui.sugchbx2)
        self.ui.sugchbx2.setText(usernamelist[1])
        suggest_checkboxlist.append(self.ui.sugchbx3)
        self.ui.sugchbx3.setText(usernamelist[2])
        suggest_checkboxlist.append(self.ui.sugchbx4)
        self.ui.sugchbx4.setText(usernamelist[3])
        suggest_checkboxlist.append(self.ui.sugchbx5)
        self.ui.sugchbx5.setText(usernamelist[4])
        #usernamelist.append(username1)
        #usernamelist.append(username2)
        #usernamelist.append(username3)
        #usernamelist.append(username4)
        #print(usernamelist)

#         for i in suggest_checkboxlist:
#            if i.checkState() == 2:
#                name = i.text()
#                print(name)
# #
        # for i in range(4):
        #     suggest_checkboxlist[i].setText(usernamelist[i])

        # for i in suggest_checkboxlist:
        #    nameofchbox = i.setText(i.text())
        # for i in suggest_checkboxlist:
        #    if i.checkState() == 2:
        #        print(i.text())

        # for i in suggest_checkboxlist:
        #    nameofchbox=i.text()
        #    print(nameofchbox)

        # if checkboxlist[0]== 2:
        #    print("this is first item in list "+ self.ui.checkBox_1.text())

    def initializeIpPort(self):
        self.ui.ip_field.setText(str(yay.SERVER_HOST_2))
        self.ui.port_field.setText(str(yay.SERVER_PORT2))
        self.ui.username_field.setText("Yasemin")
        #self.UUIDtoConnect=uuid.uuid4()

    def connect(self):
        self.get_host_with_port()
        pass

    def pubkey_button(self):
        # pubkey buttonuna basıldığında gerçekleştirilecek eylem
        request="PBKEY:"+"BUNUIMZALA"
        # myClient = yay.ClientThread("Client Thread", self.UUIDtoConnect ,self.ip, self.port, request, self.logQueue)
        myClient = yay.ClientThread("Client Thread", self.ip, self.port, request, self.logQueue)
        response = myClient.control()
        self.ui.LogLabel_field.setText("XXX"+response+"XXX")

    def refresh_feed_button(self):
        # takip edilen kişilerin serverlarına istek atarak twitleri yeniler
        if(yay.BLOG == 1):
            self.ui.Feeds_field.addItem(yay.my_mainpage)

    def send_message_button(self):
        # Send message to followed içine yazılan text yalnızca
        # followers içinde check edilen kişilere gönderilecektir
        pass

    def block_button(self):
        # Followers içindeki kullanıcılardan check edilenleri engelleyecektir.

        # request="BLOCK:"+yay.myUUID
        # # myClient = yay.ClientThread("Client Thread", self.UUIDtoConnect ,self.ip, self.port, request, self.logQueue)
        # myClient = yay.ClientThread("Client Thread", self.ip, self.port, request, self.logQueue)
        # response = myClient.control()
        # self.ui.SuggestedUser_field.addItem("XXX"+response+"XXX")
        # opp_uuid = self.findUUIDbyHostAndPort(self.ip, self.port)
        # yay.my_blacklist.append(opp_uuid)
        # self.write_to_file("MyBlacklist.json",yay.my_blacklist)
        pass

    def unblock_button(self):
        # Blocked içindeki kullanıcılardan check edilenlerin engellerini kaldıracaktır.

        # request="UNBLC:"+yay.myUUID
        # # myClient = yay.ClientThread("Client Thread", self.UUIDtoConnect ,self.ip, self.port, request, self.logQueue)
        # myClient = yay.ClientThread("Client Thread", self.ip, self.port, request, self.logQueue)
        # response = myClient.control()
        # self.ui.SuggestedUser_field.addItem("XXX"+response+"XXX")
        # opp_uuid = self.findUUIDbyHostAndPort(self.ip, self.port)
        # yay.my_followers_list.append(opp_uuid)
        # self.write_to_file("MyFollowers.json",yay.my_followers_list)
        pass

    def unsubscribe_button(self):
        # Followed içindeki kullanıcılardan check edilenleri takipten çıkacaktır.

        # request="UNSUB:"+yay.myUUID
        # # myClient = yay.ClientThread("Client Thread", self.UUIDtoConnect ,self.ip, self.port, request, self.logQueue)
        # myClient = yay.ClientThread("Client Thread", self.ip, self.port, request, self.logQueue)
        # response = myClient.control()
        # self.ui.SuggestedUser_field.addItem("XXX"+response+"XXX")
        # opp_uuid = self.findUUIDbyHostAndPort(self.ip, self.port)
        # yay.my_followed_list.remove(opp_uuid)
        # self.write_to_file("MyFollowed.json",yay.my_followed_list)
        pass

    def subscribe_button(self):
        # Suggested users içindeki kullanıcılardan check edilenleri takip edecektir.

        # request="SUBSC:"+yay.myUUID
        # # myClient = yay.ClientThread("Client Thread", self.UUIDtoConnect ,self.ip, self.port, request, self.logQueue)
        # myClient = yay.ClientThread("Client Thread", self.ip, self.port, request, self.logQueue)
        # response = myClient.control()
        # self.ui.SuggestedUser_field.addItem("XXX"+response+"XXX")
        # opp_uuid = self.findUUIDbyHostAndPort(self.ip, self.port)
        # if(response == "SUBOK"):
        #     yay.my_followed_list.append(opp_uuid)
        #     self.write_to_file("MyFollowed.json",yay.my_followed_list)

        pass
        # Suggested users içindeki kullanıcılardan check edilenleri takip edecektir.
        #followed_checkboxlist=[]
        #fldchbx1 = self.ui.fldchbx1
        #fldchbx2 = self.ui.fldchbx2
        #fldchbx3 = self.ui.fldchbx3
        #fldchbx4 = self.ui.fldchbx4
        #fldchbx5 = self.ui.fldchbx5
        #followed_checkboxlist.append(fldchbx1)
        #followed_checkboxlist.append(fldchbx2)
        #followed_checkboxlist.append(fldchbx3)
        #followed_checkboxlist.append(fldchbx4)
        #followed_checkboxlist.append(fldchbx5)
#
        #suggest_checkboxlist = []
        #suggest_checkboxlist.append(self.ui.sugchbx1)
        #suggest_checkboxlist.append(self.ui.sugchbx2)
        #suggest_checkboxlist.append(self.ui.sugchbx3)
        #suggest_checkboxlist.append(self.ui.sugchbx4)
        #suggest_checkboxlist.append(self.ui.sugchbx5)
#
        #k=0
        #for i in suggest_checkboxlist:
        #    if (i.checkState()==2):
        #        followed_checkboxlist[k].setText(i.text())
        #        k=k+1
#

    def logout_button(self):
        #logout ui kapatma olarak tasarlanmıştır. ileride connection close olarak değiştirilebilir
        self.close()

    def disable_button(self):
        self.ui.connect_button.setDisabled(True)

    def get_host_with_port(self):
       # ip ve port alma işlemi
        self.ip = self.ui.ip_field.text()
        self.port = self.ui.port_field.text()
        #self.name = self.ui.username_field.text()
        self.UUID ="AraciUUID"
        yay.userInfoDict[self.UUID]=[ self.ip,self.port,"ARACIname","NEGOTIATOR", None ]
        with open('../Yayinci_Blogger/data.json', 'w') as fp:
            json.dump(yay.userInfoDict, fp)

        name=self.ui.username_field.text()
        request="UINFO"
        myClient=yay.ClientThread("Client Thread", self.ip, self.port, request, self.logQueue)
        response=myClient.control()
        self.ui.LogLabel_field.setText("XXX" + response + "XXX")

    def change_profile_name(self):
        # kullanıcı adını bağlandığında otomatik olarak değiştirme
        username = self.ui.username_field.text()
        self.ui.UserNameLabel_field.setText(username)

    # def sendMyBlog(self):
    #     request="SBLOG:"+str(yay.myUUID)+"$"+self.ui.Twit_field.toPlainText()+"\n"
    #     # myClient = yay.ClientThread("Client Thread", self.UUIDtoConnect ,self.ip, self.port, request, self.logQueue)
    #     myClient = yay.ClientThread("Client Thread", self.ip, self.port, request, self.logQueue)
    #     response = myClient.control()
    #     self.ui.SuggestedUser_field.addItem("XXX"+response+"XXX")
    #     #opp_uuid = self.findUUIDbyHostAndPort(self.ip, self.port)

    def share_twit_button(self):
        myBlog = self.ui.Twit_field.toPlainText()+"\n"
        yay.my_blog_list.append(myBlog)
        self.sendMyBlog()
        f_myBlogs = open("Mb.txt", 'a')
        f_myBlogs.write(myBlog)
        f_myBlogs.close()
        self.ui.MyBlogList_field.addItem(myBlog)
        self.ui.Twit_field.clear()

        # myBlog = self.ui.Twit_field.toPlainText()+"\n"
        # self.ui.Feeds_field.addItem("YYYYYYYYYYYAAAAAAAAAA")
        # self.ui.Feeds_field.addItem(yay.my_blog_list)
        # #yay.my_blog_list.append(myBlog)
        # self.sendMyBlog()
        # self.write_to_file("MyBlogs.json",yay.my_blog_list)
        # self.ui.MyBlogList_field.addItem(myBlog)
        # self.ui.Twit_field.clear()
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
            serverThread = yay.ServerThread("Server Thread", c, yay.myUUID, yay.SERVER_HOST, yay.SERVER_PORT, yay.TYPE,
                                            logQueue, exitFlag)
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
