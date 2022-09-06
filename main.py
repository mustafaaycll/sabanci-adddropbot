import sys
import time
from selenium import webdriver
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
        self.setWindowTitle("Automated Course Registerer")
        self.timer = QTimer()

        self.loadMainPage()
        SU.identifyTerm()


    def loadMainPage(self):
        self.deinitializeClock()
        uic.loadUi("main.ui", self)

        self.usernameLineEdit = self.findChild(QLineEdit, "usernameLineEdit")
        self.passwordLineEdit = self.findChild(QLineEdit, "passwordLineEdit")
        self.saveButton = self.findChild(QPushButton, "saveButton")
        self.usernameLineEdit.textChanged[str].connect(lambda: self.saveButton.setEnabled(self.usernameLineEdit.text() != "" and self.passwordLineEdit.text() != ""))
        self.passwordLineEdit.textChanged[str].connect(lambda: self.saveButton.setEnabled(self.usernameLineEdit.text() != "" and self.passwordLineEdit.text() != ""))
        self.saveButton.clicked.connect(self.credentialsSaved)


    def loadSecondPage(self):
        uic.loadUi("second.ui", self)
        self.usernameField = self.findChild(QLabel, "username")
        self.passwordField = self.findChild(QLabel, "password")
        self.getBackButton = self.findChild(QPushButton, "getBackButton")
        self.visibilityButton = self.findChild(QPushButton, "visibilityButton")

        self.enrollButton = self.findChild(QPushButton, "automationButton")
        self.clearAllButton = self.findChild(QPushButton, "clearAllButton")
        self.crnEdits = []

        self.checkCrnEdit = self.findChild(QLineEdit, "checkCrnEdit")
        self.conditionalEnrollButton = self.findChild(QPushButton, "conditionalEnrollButton")
        self.conditionalEnrollButton.clicked.connect(self.conditionalAutomate)

        self.usernameField.setText(GB.USERNAME)
        self.passwordField.setText(GB.HIDDENPASSWORD)
        self.getBackButton.clicked.connect(self.loadMainPage)
        self.visibilityButton.setIcon(QIcon("assets/visibility_on.png"))
        self.visibilityButton.clicked.connect(self.visibilityToggle)
        self.enrollButton.clicked.connect(self.automate)
        self.clearAllButton.clicked.connect(self.clearCRNEdits)

        self.defineCRNEdits()
        self.initializeClock()


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
            self.visibilityButton.setIcon(QIcon("assets/visibility_off.png"))

        else:
            GB.PASSWORDVISIBILITY = True
            self.passwordField.setText(GB.HIDDENPASSWORD)
            self.visibilityButton.setIcon(QIcon("assets/visibility_on.png"))


    def clearCRNEdits(self):
        for edit in self.crnEdits:
            edit.clear()


    def defineCRNEdits(self):
        self.crn1 = self.findChild(QLineEdit, "crn1")
        self.crn1.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.crn1.text() != ""))
        self.crn1.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.crn1.text() != ""))
        self.crnEdits.append(self.crn1)
        self.crn2 = self.findChild(QLineEdit, "crn2")
        self.crn2.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.crn2.text() != ""))
        self.crn2.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.crn2.text() != ""))
        self.crnEdits.append(self.crn2)
        self.crn3 = self.findChild(QLineEdit, "crn3")
        self.crn3.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.crn3.text() != ""))
        self.crn3.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.crn3.text() != ""))
        self.crnEdits.append(self.crn3)
        self.crn4 = self.findChild(QLineEdit, "crn4")
        self.crn4.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.crn4.text() != ""))
        self.crn4.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.crn4.text() != ""))
        self.crnEdits.append(self.crn4)
        self.crn5 = self.findChild(QLineEdit, "crn5")
        self.crn5.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.crn5.text() != ""))
        self.crn5.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.crn5.text() != ""))
        self.crnEdits.append(self.crn5)
        self.crn6 = self.findChild(QLineEdit, "crn6")
        self.crn6.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.crn6.text() != ""))
        self.crn6.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.crn6.text() != ""))
        self.crnEdits.append(self.crn6)
        self.crn7 = self.findChild(QLineEdit, "crn7")
        self.crn7.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.crn7.text() != ""))
        self.crn7.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.crn7.text() != ""))
        self.crnEdits.append(self.crn7)
        self.crn8 = self.findChild(QLineEdit, "crn8")
        self.crn8.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.crn8.text() != ""))
        self.crn8.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.crn8.text() != ""))
        self.crnEdits.append(self.crn8)
        self.crn9 = self.findChild(QLineEdit, "crn9")
        self.crn9.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.crn9.text() != ""))
        self.crn9.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.crn9.text() != ""))
        self.crnEdits.append(self.crn9)
        self.crn10 = self.findChild(QLineEdit, "crn10")
        self.crn10.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.crn10.text() != ""))
        self.crn10.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.crn10.text() != ""))
        self.crnEdits.append(self.crn10)
        self.crn11 = self.findChild(QLineEdit, "crn11")
        self.crn11.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.crn11.text() != ""))
        self.crn11.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.crn11.text() != ""))
        self.crnEdits.append(self.crn11)
        self.crn12 = self.findChild(QLineEdit, "crn12")
        self.crn12.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.crn12.text() != ""))
        self.crn12.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.crn12.text() != ""))
        self.crnEdits.append(self.crn12)
        self.crn13 = self.findChild(QLineEdit, "crn13")
        self.crn13.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.crn13.text() != ""))
        self.crn13.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.crn13.text() != ""))
        self.crnEdits.append(self.crn13)
        self.crn14 = self.findChild(QLineEdit, "crn14")
        self.crn14.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.crn14.text() != ""))
        self.crn14.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.crn14.text() != ""))
        self.crnEdits.append(self.crn14)
        self.crn15 = self.findChild(QLineEdit, "crn15")
        self.crn15.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.crn15.text() != ""))
        self.crn15.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.crn15.text() != ""))
        self.crnEdits.append(self.crn15)
        self.crn16 = self.findChild(QLineEdit, "crn16")
        self.crn16.textChanged[str].connect(lambda:self.clearAllButton.setEnabled(self.crn16.text() != ""))
        self.crn16.textChanged[str].connect(lambda:self.enrollButton.setEnabled(self.crn16.text() != ""))
        self.crnEdits.append(self.crn16)


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


    def collectCRNs(self):
        for edit in self.crnEdits:
            if edit.text() != "":
                GB.CRNS.append(edit.text())


    def conditionalAutomate(self):
        try:
            browser = webdriver.Firefox()
            SU.checkUntilThereIsAvailableSeat(browser, self.checkCrnEdit.text())
            while (True):
                browser.get(GB.BANNERWEB)
                while(browser.title != "User Login"):
                    browser.get(GB.BANNERWEB)
                time.sleep(1)
                SU.login(browser, GB.USERNAME, GB.PASSWORD)
                SU.enroll(browser)
                SU.navigateToSchedule(browser, GB.USERNAME, GB.PASSWORD)
                break
        except:
            browser = None


    def automate(self):
        self.collectCRNs()
        try:
            browser = webdriver.Firefox()
            while (True):
                browser.get(GB.BANNERWEB)
                while(browser.title != "User Login"):
                    browser.get(GB.BANNERWEB)
                time.sleep(1)
                SU.login(browser, GB.USERNAME, GB.PASSWORD)
                SU.enroll(browser)
                SU.navigateToSchedule(browser, GB.USERNAME, GB.PASSWORD)
                break
        except:
            browser = None


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()