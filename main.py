import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from services import bannerWebServices as SU
import globalVars as GB

from PyQt5 import uic
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QPushButton,
)
from PyQt5.QtGui import QIcon, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(540, 249)
        self.timer = QTimer()

        self.loadMainPage()
        SU.identifyTerm()


    def loadMainPage(self):
        self.deinitializeClock()
        uic.loadUi(os.path.join(GB.BASEDIR, "ui", "main.ui"), self)

        self.imageMain = self.findChild(QLabel, "imageFirst")
        self.imageMain.setPixmap(QPixmap(os.path.join(GB.BASEDIR,"assets", "logo.png")))
        self.usernameLineEdit = self.findChild(QLineEdit, "usernameLineEdit")
        self.passwordLineEdit = self.findChild(QLineEdit, "passwordLineEdit")
        self.saveButton = self.findChild(QPushButton, "saveButton")
        self.usernameLineEdit.textChanged[str].connect(lambda: self.saveButton.setEnabled(self.usernameLineEdit.text() != "" and self.passwordLineEdit.text() != ""))
        self.passwordLineEdit.textChanged[str].connect(lambda: self.saveButton.setEnabled(self.usernameLineEdit.text() != "" and self.passwordLineEdit.text() != ""))
        self.saveButton.clicked.connect(self.credentialsSaved)


    def loadSecondPage(self):
        uic.loadUi(os.path.join(GB.BASEDIR, "ui", "second.ui"), self)
        self.imageSecond = self.findChild(QLabel, "imageSecond")
        self.imageSecond.setPixmap(QPixmap(os.path.join(GB.BASEDIR,"assets", "logo.png")))
        #info section on left
        self.usernameField = self.findChild(QLabel, "username")
        self.passwordField = self.findChild(QLabel, "password")
        self.getBackButton = self.findChild(QPushButton, "getBackButton")
        self.visibilityButton = self.findChild(QPushButton, "visibilityButton")
        self.usernameField.setText(GB.USERNAME)
        self.passwordField.setText(GB.HIDDENPASSWORD)
        self.getBackButton.clicked.connect(self.loadMainPage)
        self.visibilityButton.setIcon(QIcon(os.path.join(GB.BASEDIR, "assets", "visibility_on.png")))
        self.visibilityButton.clicked.connect(self.visibilityToggle)
        self.initializeClock()

        #elements in tab 1 on right
        self.enrollButton = self.findChild(QPushButton, "automationButton")
        self.clearAllButton = self.findChild(QPushButton, "clearAllButton")
        self.enrollButton.clicked.connect(self.tab1automate)
        self.clearAllButton.clicked.connect(self.clearCRNEdits)
        self.tab1CrnEdits = []
        self.defineTab1CRNEdits()

        #elements in tab 2 on right
        self.checkCrnEdit = self.findChild(QLineEdit, "checkCRNEdit")
        self.conditionalEnrollButton = self.findChild(QPushButton, "conditionalEnrollButton")
        self.conditionalEnrollButton.clicked.connect(self.tab2automate)
        self.tab2CrnEdits = []
        self.defineTab2CRNEdits()



    def credentialsSaved(self):
        GB.USERNAME = self.usernameLineEdit.text()
        GB.PASSWORD = self.passwordLineEdit.text()
        GB.HIDDENPASSWORD = str.join("", ["*" for i in GB.PASSWORD])
        self.usernameLineEdit.clear()
        self.passwordLineEdit.clear()
        self.loadSecondPage()


    def visibilityToggle(self):
        if GB.PASSWORDVISIBILITY == True:
            GB.PASSWORDVISIBILITY = False
            self.passwordField.setText(GB.PASSWORD)
            self.visibilityButton.setIcon(QIcon(os.path.join(GB.BASEDIR, "assets", "visibility_off.png")))

        else:
            GB.PASSWORDVISIBILITY = True
            self.passwordField.setText(GB.HIDDENPASSWORD)
            self.visibilityButton.setIcon(QIcon(os.path.join(GB.BASEDIR, "assets", "visibility_on.png")))


    def clearCRNEdits(self):
        for edit in self.tab1CrnEdits:
            edit.clear()


    def defineTab1CRNEdits(self):
        self.tab1crn1 = self.findChild(QLineEdit, "tab1crn1")
        self.tab1crn1.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.tab1crn1.text() != ""))
        self.tab1crn1.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.tab1crn1.text() != ""))
        self.tab1CrnEdits.append(self.tab1crn1)
        self.tab1crn2 = self.findChild(QLineEdit, "tab1crn2")
        self.tab1crn2.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.tab1crn2.text() != ""))
        self.tab1crn2.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.tab1crn2.text() != ""))
        self.tab1CrnEdits.append(self.tab1crn2)
        self.tab1crn3 = self.findChild(QLineEdit, "tab1crn3")
        self.tab1crn3.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.tab1crn3.text() != ""))
        self.tab1crn3.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.tab1crn3.text() != ""))
        self.tab1CrnEdits.append(self.tab1crn3)
        self.tab1crn4 = self.findChild(QLineEdit, "tab1crn4")
        self.tab1crn4.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.tab1crn4.text() != ""))
        self.tab1crn4.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.tab1crn4.text() != ""))
        self.tab1CrnEdits.append(self.tab1crn4)
        self.tab1crn5 = self.findChild(QLineEdit, "tab1crn5")
        self.tab1crn5.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.tab1crn5.text() != ""))
        self.tab1crn5.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.tab1crn5.text() != ""))
        self.tab1CrnEdits.append(self.tab1crn5)
        self.tab1crn6 = self.findChild(QLineEdit, "tab1crn6")
        self.tab1crn6.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.tab1crn6.text() != ""))
        self.tab1crn6.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.tab1crn6.text() != ""))
        self.tab1CrnEdits.append(self.tab1crn6)
        self.tab1crn7 = self.findChild(QLineEdit, "tab1crn7")
        self.tab1crn7.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.tab1crn7.text() != ""))
        self.tab1crn7.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.tab1crn7.text() != ""))
        self.tab1CrnEdits.append(self.tab1crn7)
        self.tab1crn8 = self.findChild(QLineEdit, "tab1crn8")
        self.tab1crn8.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.tab1crn8.text() != ""))
        self.tab1crn8.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.tab1crn8.text() != ""))
        self.tab1CrnEdits.append(self.tab1crn8)
        self.tab1crn9 = self.findChild(QLineEdit, "tab1crn9")
        self.tab1crn9.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.tab1crn9.text() != ""))
        self.tab1crn9.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.tab1crn9.text() != ""))
        self.tab1CrnEdits.append(self.tab1crn9)
        self.tab1crn10 = self.findChild(QLineEdit, "tab1crn10")
        self.tab1crn10.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.tab1crn10.text() != ""))
        self.tab1crn10.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.tab1crn10.text() != ""))
        self.tab1CrnEdits.append(self.tab1crn10)
        self.tab1crn11 = self.findChild(QLineEdit, "tab1crn11")
        self.tab1crn11.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.tab1crn11.text() != ""))
        self.tab1crn11.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.tab1crn11.text() != ""))
        self.tab1CrnEdits.append(self.tab1crn11)
        self.tab1crn12 = self.findChild(QLineEdit, "tab1crn12")
        self.tab1crn12.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.tab1crn12.text() != ""))
        self.tab1crn12.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.tab1crn12.text() != ""))
        self.tab1CrnEdits.append(self.tab1crn12)
        self.tab1crn13 = self.findChild(QLineEdit, "tab1crn13")
        self.tab1crn13.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.tab1crn13.text() != ""))
        self.tab1crn13.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.tab1crn13.text() != ""))
        self.tab1CrnEdits.append(self.tab1crn13)
        self.tab1crn14 = self.findChild(QLineEdit, "tab1crn14")
        self.tab1crn14.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.tab1crn14.text() != ""))
        self.tab1crn14.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.tab1crn14.text() != ""))
        self.tab1CrnEdits.append(self.tab1crn14)
        self.tab1crn15 = self.findChild(QLineEdit, "tab1crn15")
        self.tab1crn15.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.tab1crn15.text() != ""))
        self.tab1crn15.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.tab1crn15.text() != ""))
        self.tab1CrnEdits.append(self.tab1crn15)
        self.tab1crn16 = self.findChild(QLineEdit, "tab1crn16")
        self.tab1crn16.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.tab1crn16.text() != ""))
        self.tab1crn16.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.tab1crn16.text() != ""))
        self.tab1CrnEdits.append(self.tab1crn16)


    def defineTab2CRNEdits(self):
        self.tab2crn1 = self.findChild(QLineEdit, "tab2crn1")
        self.tab2crn1.textChanged[str].connect(lambda:self.conditionalEnrollButton.setEnabled(self.tab2crn1.text() != "" and self.checkCrnEdit.text() != ""))
        self.tab2CrnEdits.append(self.tab2crn1)
        self.tab2crn2 = self.findChild(QLineEdit, "tab2crn2")
        self.tab2crn2.textChanged[str].connect(lambda:self.conditionalEnrollButton.setEnabled(self.tab2crn2.text() != "" and self.checkCrnEdit.text() != ""))
        self.tab2CrnEdits.append(self.tab2crn2)
        self.tab2crn3 = self.findChild(QLineEdit, "tab2crn3")
        self.tab2crn3.textChanged[str].connect(lambda:self.conditionalEnrollButton.setEnabled(self.tab2crn3.text() != "" and self.checkCrnEdit.text() != ""))
        self.tab2CrnEdits.append(self.tab2crn3)
        self.tab2crn4 = self.findChild(QLineEdit, "tab2crn4")
        self.tab2crn4.textChanged[str].connect(lambda:self.conditionalEnrollButton.setEnabled(self.tab2crn4.text() != "" and self.checkCrnEdit.text() != ""))
        self.tab2CrnEdits.append(self.tab2crn4)
        self.tab2crn5 = self.findChild(QLineEdit, "tab2crn5")
        self.tab2crn5.textChanged[str].connect(lambda:self.conditionalEnrollButton.setEnabled(self.tab2crn5.text() != "" and self.checkCrnEdit.text() != ""))
        self.tab2CrnEdits.append(self.tab2crn5)
        self.tab2crn6 = self.findChild(QLineEdit, "tab2crn6")
        self.tab2crn6.textChanged[str].connect(lambda:self.conditionalEnrollButton.setEnabled(self.tab2crn6.text() != "" and self.checkCrnEdit.text() != ""))
        self.tab2CrnEdits.append(self.tab2crn6)
        self.tab2crn7 = self.findChild(QLineEdit, "tab2crn7")
        self.tab2crn7.textChanged[str].connect(lambda:self.conditionalEnrollButton.setEnabled(self.tab2crn7.text() != "" and self.checkCrnEdit.text() != ""))
        self.tab2CrnEdits.append(self.tab2crn7)
        self.tab2crn8 = self.findChild(QLineEdit, "tab2crn8")
        self.tab2crn8.textChanged[str].connect(lambda:self.conditionalEnrollButton.setEnabled(self.tab2crn8.text() != "" and self.checkCrnEdit.text() != ""))
        self.tab2CrnEdits.append(self.tab2crn8)
        self.checkCrnEdit.textChanged[str].connect(lambda:self.conditionalEnrollButton.setEnabled(self.checkCrnEdit.text() != "" and self.checkAnyTab2CrnEditHasText()))


    def checkAnyTab2CrnEditHasText(self):
        for edit in self.tab2CrnEdits:
            if edit.text() != "":
                return True
        return False


    def initializeClock(self):
        self.timer.blockSignals(False)
        self.timer.timeout.connect(self.updateClock)
        self.timer.start(100)


    def deinitializeClock(self):
        self.timer.blockSignals(True)


    def updateClock(self):
        self.currentTime = QTime.currentTime()
        self.stringTime = self.currentTime.toString("hh:mm:ss")
        self.clock = self.findChild(QLCDNumber, "clock")
        self.clock.display(self.stringTime)


    def tab1CollectCRNs(self):
        GB.CRNS = []
        for edit in self.tab1CrnEdits:
            if edit.text() != "":
                GB.CRNS.append(edit.text())


    def tab2CollectCRNs(self):
        GB.CRNS = []
        for edit in self.tab2CrnEdits:
            if edit.text() != "":
                GB.CRNS.append(edit.text())


    def tab2automate(self):
        self.tab2CollectCRNs()
        try:
            caps = DesiredCapabilities().CHROME
            caps["pageLoadStrategy"] = "eager"
            browser = webdriver.Chrome(service=Service(SU.resource_path(GB.DRIVERPATH)), desired_capabilities=caps)
            SU.checkUntilThereIsAvailableSeat(browser, self.checkCrnEdit.text())
            while (True):
                browser.get(GB.BANNERWEB)
                while(browser.title != "User Login"):
                    browser.get(GB.BANNERWEB)
                time.sleep(0.2)
                SU.login(browser)
                SU.enroll(browser)
                SU.navigateToSchedule(browser)
                break
        except:
            browser = None


    def tab1automate(self):
        self.tab1CollectCRNs()
        try:
            caps = DesiredCapabilities().CHROME
            caps["pageLoadStrategy"] = "eager"
            browser = webdriver.Chrome(service=Service(SU.resource_path(GB.DRIVERPATH)), desired_capabilities=caps)
            while (True):
                browser.get(GB.BANNERWEB)
                while(browser.title != "User Login"):
                    browser.get(GB.BANNERWEB)
                time.sleep(0.2)
                SU.login(browser)
                SU.enroll(browser)
                SU.navigateToSchedule(browser)
                break
        except:
            browser = None


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()