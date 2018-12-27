from PyQt5 import QtWidgets, QtGui
import sys

from QT5_önyüz.dagitik_proje_ui import Ui_MainWindow
my_blog_list =[]

class Test_Ui(QtWidgets.QMainWindow):
    def __init__(self):
        self.qt_app = QtWidgets.QApplication(sys.argv)
        QtWidgets.QWidget.__init__(self, None)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        list1 =[]
        self.ui.pushButton.pressed.connect(self.get_host_with_port)
        self.ui.pushButton.pressed.connect(self.change_profile_name)
        self.ui.pushButton_5.pressed.connect(self.share_twit)

    def get_host_with_port(self):

        # ip ve port alma işlemi
        ip = self.ui.plainTextEdit.toPlainText()
        port = self.ui.plainTextEdit_2.toPlainText()
        # self.ui.plainTextEdit_2.setPlainText(ip)

    def change_profile_name(self):
        # kullanıcı adını bağlandığında otomatik olarak değiştirme

        # username =  name parametresi çekilecek
        # username= self.ui.plainTextEdit.toPlainText()
        # self.ui.label_2.setText(username)
        pass

    def share_twit(self):
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

    def suggest_user(self, number_of_suggest, userlist):
        # sayıya göre kullanıcı öneri listesini gösterme
        self.number_of_suggest = number_of_suggest
        self.userlist = userlist
        if userlist is None:
            error_notification = 'Baglananan kullanıcı bulunmamaktadır.'
            self.ui.listWidget_6.addItems(error_notification)



    def run(self):
        self.show()
        self.qt_app.exec_()


def main():
    app = Test_Ui()
    app.run()


if __name__ == '__main__':
    main()
