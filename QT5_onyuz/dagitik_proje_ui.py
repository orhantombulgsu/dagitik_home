# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dagitik_proje.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(935, 504)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.Twit_field = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.Twit_field.setObjectName("Twit_field")
        self.gridLayout.addWidget(self.Twit_field, 3, 0, 1, 5)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 5, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.UserNameLabel_field = QtWidgets.QLabel(self.centralwidget)
        self.UserNameLabel_field.setObjectName("UserNameLabel_field")
        self.gridLayout.addWidget(self.UserNameLabel_field, 1, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 2, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 5, 1, 3)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 8, 1, 4)
        self.connect_button = QtWidgets.QPushButton(self.centralwidget)
        self.connect_button.setObjectName("connect_button")
        self.gridLayout.addWidget(self.connect_button, 0, 13, 1, 1)
        self.LogOut_button = QtWidgets.QPushButton(self.centralwidget)
        self.LogOut_button.setObjectName("LogOut_button")
        self.gridLayout.addWidget(self.LogOut_button, 0, 14, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(27)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 0, 0, 1, 4)
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 2, 12, 1, 1)
        self.SuggestedUser_field = QtWidgets.QListWidget(self.centralwidget)
        self.SuggestedUser_field.setObjectName("SuggestedUser_field")
        self.gridLayout.addWidget(self.SuggestedUser_field, 3, 5, 4, 3)
        self.Followed_field = QtWidgets.QListWidget(self.centralwidget)
        self.Followed_field.setObjectName("Followed_field")
        self.gridLayout.addWidget(self.Followed_field, 3, 8, 4, 4)
        self.Inbox_field = QtWidgets.QListView(self.centralwidget)
        self.Inbox_field.setObjectName("Inbox_field")
        self.gridLayout.addWidget(self.Inbox_field, 3, 12, 7, 3)
        self.Share_button = QtWidgets.QPushButton(self.centralwidget)
        self.Share_button.setObjectName("Share_button")
        self.gridLayout.addWidget(self.Share_button, 4, 4, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 5, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 5, 3, 1, 1)
        self.Feeds_field = QtWidgets.QListWidget(self.centralwidget)
        self.Feeds_field.setObjectName("Feeds_field")
        self.gridLayout.addWidget(self.Feeds_field, 6, 0, 6, 3)
        self.MyBlogList_field = QtWidgets.QListWidget(self.centralwidget)
        self.MyBlogList_field.setObjectName("MyBlogList_field")
        self.gridLayout.addWidget(self.MyBlogList_field, 6, 3, 6, 2)
        self.Subscribe_button = QtWidgets.QPushButton(self.centralwidget)
        self.Subscribe_button.setObjectName("Subscribe_button")
        self.gridLayout.addWidget(self.Subscribe_button, 7, 5, 1, 3)
        self.UnSubscribe_button = QtWidgets.QPushButton(self.centralwidget)
        self.UnSubscribe_button.setObjectName("UnSubscribe_button")
        self.gridLayout.addWidget(self.UnSubscribe_button, 7, 8, 1, 4)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 8, 5, 1, 3)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 8, 8, 1, 4)
        self.Blocked_field = QtWidgets.QListWidget(self.centralwidget)
        self.Blocked_field.setObjectName("Blocked_field")
        self.gridLayout.addWidget(self.Blocked_field, 9, 5, 3, 3)
        self.Followers_field = QtWidgets.QListWidget(self.centralwidget)
        self.Followers_field.setObjectName("Followers_field")
        self.gridLayout.addWidget(self.Followers_field, 9, 8, 3, 4)
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 10, 12, 1, 3)
        self.SendMessage_field = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.SendMessage_field.setObjectName("SendMessage_field")
        self.gridLayout.addWidget(self.SendMessage_field, 11, 12, 1, 3)
        self.RefleshtheFeeds_button = QtWidgets.QPushButton(self.centralwidget)
        self.RefleshtheFeeds_button.setObjectName("RefleshtheFeeds_button")
        self.gridLayout.addWidget(self.RefleshtheFeeds_button, 12, 2, 1, 1)
        self.UnBlock_button = QtWidgets.QPushButton(self.centralwidget)
        self.UnBlock_button.setObjectName("UnBlock_button")
        self.gridLayout.addWidget(self.UnBlock_button, 12, 5, 1, 3)
        self.Block_button = QtWidgets.QPushButton(self.centralwidget)
        self.Block_button.setObjectName("Block_button")
        self.gridLayout.addWidget(self.Block_button, 12, 8, 1, 4)
        self.SendMessage_button = QtWidgets.QPushButton(self.centralwidget)
        self.SendMessage_button.setObjectName("SendMessage_button")
        self.gridLayout.addWidget(self.SendMessage_button, 12, 13, 1, 2)
        self.ip_field = QtWidgets.QLineEdit(self.centralwidget)
        self.ip_field.setObjectName("ip_field")
        self.gridLayout.addWidget(self.ip_field, 0, 6, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 0, 8, 1, 1)
        self.port_field = QtWidgets.QLineEdit(self.centralwidget)
        self.port_field.setObjectName("port_field")
        self.gridLayout.addWidget(self.port_field, 0, 9, 1, 4)
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 1, 5, 1, 1)
        self.username_field = QtWidgets.QLineEdit(self.centralwidget)
        self.username_field.setObjectName("username_field")
        self.gridLayout.addWidget(self.username_field, 1, 6, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 935, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_7.setText(_translate("MainWindow", "Ip"))
        self.label.setText(_translate("MainWindow", "Profile :"))
        self.UserNameLabel_field.setText(_translate("MainWindow", "Name"))
        self.label_10.setText(_translate("MainWindow", "What\'s happening ?"))
        self.label_3.setText(_translate("MainWindow", "Suggestted Users"))
        self.label_4.setText(_translate("MainWindow", "Followed"))
        self.connect_button.setText(_translate("MainWindow", "Connect"))
        self.LogOut_button.setText(_translate("MainWindow", "LogOut"))
        self.label_14.setText(_translate("MainWindow", "TWITTER from Group4"))
        self.label_13.setText(_translate("MainWindow", "Inbox "))
        self.Share_button.setText(_translate("MainWindow", "Share"))
        self.label_9.setText(_translate("MainWindow", "Feeds"))
        self.label_11.setText(_translate("MainWindow", "My Blog List"))
        self.Subscribe_button.setText(_translate("MainWindow", "Subscribe"))
        self.UnSubscribe_button.setText(_translate("MainWindow", "UnSubscribe"))
        self.label_5.setText(_translate("MainWindow", "Blocked"))
        self.label_6.setText(_translate("MainWindow", "Followers"))
        self.label_12.setText(_translate("MainWindow", "Send Message to Followed"))
        self.RefleshtheFeeds_button.setText(_translate("MainWindow", "Refresh the Feeds"))
        self.UnBlock_button.setText(_translate("MainWindow", "UnBlock"))
        self.Block_button.setText(_translate("MainWindow", "Block"))
        self.SendMessage_button.setText(_translate("MainWindow", "Send Message"))
        self.label_8.setText(_translate("MainWindow", "Port"))
        self.label_15.setText(_translate("MainWindow", "UserName"))

