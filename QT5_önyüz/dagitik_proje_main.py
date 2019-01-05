from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from Aracı_Negotiator import Araci_with_2_threads, Araci_with_2_threads_Logger
from QT5_önyüz.dagitik_proje_ui import Ui_MainWindow
import threading
my_blog_list = []



class ProjectUi(QtWidgets.QMainWindow):
    def __init__(self):
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
        ip = self.ui.lineEdit.text()
        port = self.ui.lineEdit_2.text()
        name = self.ui.lineEdit_3.text()

        #self.ui.plainTextEdit_4.setPlainText(i)

        for i in range(10):
           self.ui.listWidget.addItem('Item %s' %(i+1))

        #item = QtGui.QListWidgetItem()
        item = QtWidgets.QListWidgetItem
        item.setText(QtGui.QGuiApplication.translate("Dialog",'x',None,))
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.listWidget.addItem(item)

    def change_profile_name(self):
        # kullanıcı adını bağlandığında otomatik olarak değiştirme

        # username =  name parametresi çekilecek
        # username= self.ui.plainTextEdit.toPlainText()
        # self.ui.label_2.setText(username)
        pass

    def share_twit_button(self):
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


def main():
    app = ProjectUi()
    app.run()


if __name__ == '__main__':
    main()
