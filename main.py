import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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


def createBrowser():
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"
    options = Options()
    options.add_experimental_option("detach", True)
    return webdriver.Chrome(service=Service(SU.resource_path(GB.DRIVERPATH)), desired_capabilities=caps, options=options)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(683, 249)
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

        #elements in FORCE ENTRY (FE) tab
        self.FEstartButton = self.findChild(QPushButton, "FEstartButton")
        self.FEstartButton.clicked.connect(self.FEautomate)


        #elements in JUST ADD (JA) tab
        self.JAstartButton = self.findChild(QPushButton, "JAstartButton")
        self.JAclearButton = self.findChild(QPushButton, "JAclearButton")
        self.JAstartButton.clicked.connect(self.JAautomate)
        self.JAclearButton.clicked.connect(self.clearCRNEdits)
        self.JAcrnEdits = []
        self.defineJAcrnEdits()

        #elements in CHECK AND ADD (CA) tab
        self.CAcrnCheck = self.findChild(QLineEdit, "CAcrnCheck")
        self.CAstartButton = self.findChild(QPushButton, "CAstartButton")
        self.CAstartButton.clicked.connect(self.CAautomate)
        self.CAcrnEdits = []
        self.defineCAcrnEdits()

        #elements in DROP AND ADD (DA) tab
        self.DAstartButton = self.findChild(QPushButton, "DAstartButton")
        self.DAstartButton.clicked.connect(self.DAautomate)
        self.DAdropcrnEdits = []
        self.DAaddcrnEdits = []
        self.defineDAcrnEdits()


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
        for edit in self.JAcrnEdits:
            edit.clear()


    def defineJAcrnEdits(self):
        self.JAcrn1 = self.findChild(QLineEdit, "JAcrn1")
        self.JAcrn1.textChanged[str].connect(lambda:self.JAclearButton.setEnabled(self.JAclearButtonisEligibleToBeEnabled()))
        self.JAcrn1.textChanged[str].connect(lambda:self.JAstartButton.setEnabled(self.JAstartButtonisEligibleToBeEnabled()))
        self.JAcrnEdits.append(self.JAcrn1)
        self.JAcrn2 = self.findChild(QLineEdit, "JAcrn2")
        self.JAcrn2.textChanged[str].connect(lambda:self.JAclearButton.setEnabled(self.JAclearButtonisEligibleToBeEnabled()))
        self.JAcrn2.textChanged[str].connect(lambda:self.JAstartButton.setEnabled(self.JAstartButtonisEligibleToBeEnabled()))
        self.JAcrnEdits.append(self.JAcrn2)
        self.JAcrn3 = self.findChild(QLineEdit, "JAcrn3")
        self.JAcrn3.textChanged[str].connect(lambda:self.JAclearButton.setEnabled(self.JAclearButtonisEligibleToBeEnabled()))
        self.JAcrn3.textChanged[str].connect(lambda:self.JAstartButton.setEnabled(self.JAstartButtonisEligibleToBeEnabled()))
        self.JAcrnEdits.append(self.JAcrn3)
        self.JAcrn4 = self.findChild(QLineEdit, "JAcrn4")
        self.JAcrn4.textChanged[str].connect(lambda:self.JAclearButton.setEnabled(self.JAclearButtonisEligibleToBeEnabled()))
        self.JAcrn4.textChanged[str].connect(lambda:self.JAstartButton.setEnabled(self.JAstartButtonisEligibleToBeEnabled()))
        self.JAcrnEdits.append(self.JAcrn4)
        self.JAcrn5 = self.findChild(QLineEdit, "JAcrn5")
        self.JAcrn5.textChanged[str].connect(lambda:self.JAclearButton.setEnabled(self.JAclearButtonisEligibleToBeEnabled()))
        self.JAcrn5.textChanged[str].connect(lambda:self.JAstartButton.setEnabled(self.JAstartButtonisEligibleToBeEnabled()))
        self.JAcrnEdits.append(self.JAcrn5)
        self.JAcrn6 = self.findChild(QLineEdit, "JAcrn6")
        self.JAcrn6.textChanged[str].connect(lambda:self.JAclearButton.setEnabled(self.JAclearButtonisEligibleToBeEnabled()))
        self.JAcrn6.textChanged[str].connect(lambda:self.JAstartButton.setEnabled(self.JAstartButtonisEligibleToBeEnabled()))
        self.JAcrnEdits.append(self.JAcrn6)
        self.JAcrn7 = self.findChild(QLineEdit, "JAcrn7")
        self.JAcrn7.textChanged[str].connect(lambda:self.JAclearButton.setEnabled(self.JAclearButtonisEligibleToBeEnabled()))
        self.JAcrn7.textChanged[str].connect(lambda:self.JAstartButton.setEnabled(self.JAstartButtonisEligibleToBeEnabled()))
        self.JAcrnEdits.append(self.JAcrn7)
        self.JAcrn8 = self.findChild(QLineEdit, "JAcrn8")
        self.JAcrn8.textChanged[str].connect(lambda:self.JAclearButton.setEnabled(self.JAclearButtonisEligibleToBeEnabled()))
        self.JAcrn8.textChanged[str].connect(lambda:self.JAstartButton.setEnabled(self.JAstartButtonisEligibleToBeEnabled()))
        self.JAcrnEdits.append(self.JAcrn8)
        self.JAcrn9 = self.findChild(QLineEdit, "JAcrn9")
        self.JAcrn9.textChanged[str].connect(lambda:self.JAclearButton.setEnabled(self.JAclearButtonisEligibleToBeEnabled()))
        self.JAcrn9.textChanged[str].connect(lambda:self.JAstartButton.setEnabled(self.JAstartButtonisEligibleToBeEnabled()))
        self.JAcrnEdits.append(self.JAcrn9)
        self.JAcrn10 = self.findChild(QLineEdit, "JAcrn10")
        self.JAcrn10.textChanged[str].connect(lambda:self.JAclearButton.setEnabled(self.JAclearButtonisEligibleToBeEnabled()))
        self.JAcrn10.textChanged[str].connect(lambda:self.JAstartButton.setEnabled(self.JAstartButtonisEligibleToBeEnabled()))
        self.JAcrnEdits.append(self.JAcrn10)
        self.JAcrn11 = self.findChild(QLineEdit, "JAcrn11")
        self.JAcrn11.textChanged[str].connect(lambda:self.JAclearButton.setEnabled(self.JAclearButtonisEligibleToBeEnabled()))
        self.JAcrn11.textChanged[str].connect(lambda:self.JAstartButton.setEnabled(self.JAstartButtonisEligibleToBeEnabled()))
        self.JAcrnEdits.append(self.JAcrn11)
        self.JAcrn12 = self.findChild(QLineEdit, "JAcrn12")
        self.JAcrn12.textChanged[str].connect(lambda:self.JAclearButton.setEnabled(self.JAclearButtonisEligibleToBeEnabled()))
        self.JAcrn12.textChanged[str].connect(lambda:self.JAstartButton.setEnabled(self.JAstartButtonisEligibleToBeEnabled()))
        self.JAcrnEdits.append(self.JAcrn12)
        self.JAcrn13 = self.findChild(QLineEdit, "JAcrn13")
        self.JAcrn13.textChanged[str].connect(lambda:self.JAclearButton.setEnabled(self.JAclearButtonisEligibleToBeEnabled()))
        self.JAcrn13.textChanged[str].connect(lambda:self.JAstartButton.setEnabled(self.JAstartButtonisEligibleToBeEnabled()))
        self.JAcrnEdits.append(self.JAcrn13)
        self.JAcrn14 = self.findChild(QLineEdit, "JAcrn14")
        self.JAcrn14.textChanged[str].connect(lambda:self.JAclearButton.setEnabled(self.JAclearButtonisEligibleToBeEnabled()))
        self.JAcrn14.textChanged[str].connect(lambda:self.JAstartButton.setEnabled(self.JAstartButtonisEligibleToBeEnabled()))
        self.JAcrnEdits.append(self.JAcrn14)
        self.JAcrn15 = self.findChild(QLineEdit, "JAcrn15")
        self.JAcrn15.textChanged[str].connect(lambda:self.JAclearButton.setEnabled(self.JAclearButtonisEligibleToBeEnabled()))
        self.JAcrn15.textChanged[str].connect(lambda:self.JAstartButton.setEnabled(self.JAstartButtonisEligibleToBeEnabled()))
        self.JAcrnEdits.append(self.JAcrn15)
        self.JAcrn16 = self.findChild(QLineEdit, "JAcrn16")
        self.JAcrn16.textChanged[str].connect(lambda:self.JAclearButton.setEnabled(self.JAclearButtonisEligibleToBeEnabled()))
        self.JAcrn16.textChanged[str].connect(lambda:self.JAstartButton.setEnabled(self.JAstartButtonisEligibleToBeEnabled()))
        self.JAcrnEdits.append(self.JAcrn16)


    def defineCAcrnEdits(self):
        self.CAcrn1 = self.findChild(QLineEdit, "CAcrn1")
        self.CAcrn1.textChanged[str].connect(lambda:self.CAstartButton.setEnabled(self.CAstartButtonisEligibleToBeEnabled()))
        self.CAcrnEdits.append(self.CAcrn1)
        self.CAcrn2 = self.findChild(QLineEdit, "CAcrn2")
        self.CAcrn2.textChanged[str].connect(lambda:self.CAstartButton.setEnabled(self.CAstartButtonisEligibleToBeEnabled()))
        self.CAcrnEdits.append(self.CAcrn2)
        self.CAcrn3 = self.findChild(QLineEdit, "CAcrn3")
        self.CAcrn3.textChanged[str].connect(lambda:self.CAstartButton.setEnabled(self.CAstartButtonisEligibleToBeEnabled()))
        self.CAcrnEdits.append(self.CAcrn3)
        self.CAcrn4 = self.findChild(QLineEdit, "CAcrn4")
        self.CAcrn4.textChanged[str].connect(lambda:self.CAstartButton.setEnabled(self.CAstartButtonisEligibleToBeEnabled()))
        self.CAcrnEdits.append(self.CAcrn4)
        self.CAcrn5 = self.findChild(QLineEdit, "CAcrn5")
        self.CAcrn5.textChanged[str].connect(lambda:self.CAstartButton.setEnabled(self.CAstartButtonisEligibleToBeEnabled()))
        self.CAcrnEdits.append(self.CAcrn5)
        self.CAcrn6 = self.findChild(QLineEdit, "CAcrn6")
        self.CAcrn6.textChanged[str].connect(lambda:self.CAstartButton.setEnabled(self.CAstartButtonisEligibleToBeEnabled()))
        self.CAcrnEdits.append(self.CAcrn6)
        self.CAcrn7 = self.findChild(QLineEdit, "CAcrn7")
        self.CAcrn7.textChanged[str].connect(lambda:self.CAstartButton.setEnabled(self.CAstartButtonisEligibleToBeEnabled()))
        self.CAcrnEdits.append(self.CAcrn7)
        self.CAcrn8 = self.findChild(QLineEdit, "CAcrn8")
        self.CAcrn8.textChanged[str].connect(lambda:self.CAstartButton.setEnabled(self.CAstartButtonisEligibleToBeEnabled()))
        self.CAcrnEdits.append(self.CAcrn8)
        self.CAcrnCheck.textChanged[str].connect(lambda:self.CAstartButton.setEnabled(self.CAstartButtonisEligibleToBeEnabled()))


    def defineDAcrnEdits(self):
        self.DAdropcrn1 = self.findChild(QLineEdit, "DAdropcrn1")
        self.DAdropcrn1.textChanged[str].connect(lambda:self.DAstartButton.setEnabled(self.DAstartButtonisEligibleToBeEnabled()))
        self.DAdropcrnEdits.append(self.DAdropcrn1)
        self.DAdropcrn2 = self.findChild(QLineEdit, "DAdropcrn2")
        self.DAdropcrn2.textChanged[str].connect(lambda:self.DAstartButton.setEnabled(self.DAstartButtonisEligibleToBeEnabled()))
        self.DAdropcrnEdits.append(self.DAdropcrn2)
        self.DAdropcrn3 = self.findChild(QLineEdit, "DAdropcrn3")
        self.DAdropcrn3.textChanged[str].connect(lambda:self.DAstartButton.setEnabled(self.DAstartButtonisEligibleToBeEnabled()))
        self.DAdropcrnEdits.append(self.DAdropcrn3)
        self.DAdropcrn4 = self.findChild(QLineEdit, "DAdropcrn4")
        self.DAdropcrn4.textChanged[str].connect(lambda:self.DAstartButton.setEnabled(self.DAstartButtonisEligibleToBeEnabled()))
        self.DAdropcrnEdits.append(self.DAdropcrn4)
        self.DAdropcrn5 = self.findChild(QLineEdit, "DAdropcrn5")
        self.DAdropcrn5.textChanged[str].connect(lambda:self.DAstartButton.setEnabled(self.DAstartButtonisEligibleToBeEnabled()))
        self.DAdropcrnEdits.append(self.DAdropcrn5)
        self.DAdropcrn6 = self.findChild(QLineEdit, "DAdropcrn6")
        self.DAdropcrn6.textChanged[str].connect(lambda:self.DAstartButton.setEnabled(self.DAstartButtonisEligibleToBeEnabled()))
        self.DAdropcrnEdits.append(self.DAdropcrn6)
        self.DAdropcrn7 = self.findChild(QLineEdit, "DAdropcrn7")
        self.DAdropcrn7.textChanged[str].connect(lambda:self.DAstartButton.setEnabled(self.DAstartButtonisEligibleToBeEnabled()))
        self.DAdropcrnEdits.append(self.DAdropcrn7)
        self.DAdropcrn8 = self.findChild(QLineEdit, "DAdropcrn8")
        self.DAdropcrn8.textChanged[str].connect(lambda:self.DAstartButton.setEnabled(self.DAstartButtonisEligibleToBeEnabled()))
        self.DAdropcrnEdits.append(self.DAdropcrn8)

        self.DAaddcrn1 = self.findChild(QLineEdit, "DAaddcrn1")
        self.DAaddcrn1.textChanged[str].connect(lambda:self.DAstartButton.setEnabled(self.DAstartButtonisEligibleToBeEnabled()))
        self.DAaddcrnEdits.append(self.DAaddcrn1)
        self.DAaddcrn2 = self.findChild(QLineEdit, "DAaddcrn2")
        self.DAaddcrn2.textChanged[str].connect(lambda:self.DAstartButton.setEnabled(self.DAstartButtonisEligibleToBeEnabled()))
        self.DAaddcrnEdits.append(self.DAaddcrn2)
        self.DAaddcrn3 = self.findChild(QLineEdit, "DAaddcrn3")
        self.DAaddcrn3.textChanged[str].connect(lambda:self.DAstartButton.setEnabled(self.DAstartButtonisEligibleToBeEnabled()))
        self.DAaddcrnEdits.append(self.DAaddcrn3)
        self.DAaddcrn4 = self.findChild(QLineEdit, "DAaddcrn4")
        self.DAaddcrn4.textChanged[str].connect(lambda:self.DAstartButton.setEnabled(self.DAstartButtonisEligibleToBeEnabled()))
        self.DAaddcrnEdits.append(self.DAaddcrn4)
        self.DAaddcrn5 = self.findChild(QLineEdit, "DAaddcrn5")
        self.DAaddcrn5.textChanged[str].connect(lambda:self.DAstartButton.setEnabled(self.DAstartButtonisEligibleToBeEnabled()))
        self.DAaddcrnEdits.append(self.DAaddcrn5)
        self.DAaddcrn6 = self.findChild(QLineEdit, "DAaddcrn6")
        self.DAaddcrn6.textChanged[str].connect(lambda:self.DAstartButton.setEnabled(self.DAstartButtonisEligibleToBeEnabled()))
        self.DAaddcrnEdits.append(self.DAaddcrn6)
        self.DAaddcrn7 = self.findChild(QLineEdit, "DAaddcrn7")
        self.DAaddcrn7.textChanged[str].connect(lambda:self.DAstartButton.setEnabled(self.DAstartButtonisEligibleToBeEnabled()))
        self.DAaddcrnEdits.append(self.DAaddcrn7)
        self.DAaddcrn8 = self.findChild(QLineEdit, "DAaddcrn8")
        self.DAaddcrn8.textChanged[str].connect(lambda:self.DAstartButton.setEnabled(self.DAstartButtonisEligibleToBeEnabled()))
        self.DAaddcrnEdits.append(self.DAaddcrn8)


    def JAclearButtonisEligibleToBeEnabled(self):
        for edit in self.JAcrnEdits:
            if edit.text() != "":
                return True
        return False


    def JAstartButtonisEligibleToBeEnabled(self):
        for edit in self.JAcrnEdits:
            if edit.text() != "":
                return True
        return False


    def CAstartButtonisEligibleToBeEnabled(self):
        for addedit in self.CAcrnEdits:
            if addedit.text() != "":
                if self.CAcrnCheck.text() != "":
                    return True
        return False


    def DAstartButtonisEligibleToBeEnabled(self):
        for dropedit in self.DAdropcrnEdits:
            if dropedit.text() != "":
                for addedit in self.DAaddcrnEdits:
                    if addedit.text() != "":
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


    def JAcollectCRNs(self):
        GB.CRNSTOADD = []
        for edit in self.JAcrnEdits:
            if edit.text() != "":
                GB.CRNSTOADD.append(edit.text())


    def CAcollectCRNs(self):
        GB.CRNSTOADD = []
        for edit in self.CAcrnEdits:
            if edit.text() != "":
                GB.CRNSTOADD.append(edit.text())


    def DAcollectCRNs(self):
        GB.CRNSTODROP = []
        for edit in self.DAdropcrnEdits:
            if edit.text() != "":
                GB.CRNSTODROP.append(edit.text())

        GB.CRNSTOADD = []
        for edit in self.DAaddcrnEdits:
            if edit.text() != "":
                GB.CRNSTOADD.append(edit.text())


    def FEautomate(self):
        try:
            browser = createBrowser()
            browser.get(GB.BANNERWEB)
            while(browser.title != "User Login"):
                time.sleep(0.5)
                browser.get(GB.BANNERWEB)
            time.sleep(0.2)
            SU.login(browser)
            SU.openAddDropPage(browser)
        except:
            browser = None


    def JAautomate(self):
        self.JAcollectCRNs()
        try:
            browser = createBrowser()
            browser.get(GB.BANNERWEB)
            while(browser.title != "User Login"):
                time.sleep(0.5)
                browser.get(GB.BANNERWEB)
            time.sleep(0.2)
            SU.login(browser)
            SU.enroll(browser)
            time.sleep(15)
            SU.navigateToSchedule(browser)
        except:
            browser = None


    def CAautomate(self):
        self.CAcollectCRNs()
        try:
            browser = createBrowser()
            SU.checkUntilThereIsAvailableSeat(browser, self.CAcrnCheck.text())
            browser.get(GB.BANNERWEB)
            while(browser.title != "User Login"):
                time.sleep(0.5)
                browser.get(GB.BANNERWEB)
            time.sleep(0.2)
            SU.login(browser)
            SU.enroll(browser)
            time.sleep(15)
            SU.navigateToSchedule(browser)
        except:
            browser = None


    def DAautomate(self):
        self.DAcollectCRNs()
        print("drop crns: ", [i.text() for i in self.DAdropcrnEdits])
        print("add crns: ", [i.text() for i in self.DAaddcrnEdits])
        print("COLLECTED drop crns: ", GB.CRNSTODROP)
        print("COLLECTED add crns: ", GB.CRNSTOADD)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()