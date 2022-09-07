from datetime import date
import os
import sys
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import globalVars as GB

class bannerWebServices():
    def resource_path(relative_path: str) -> str:
        try:
            base_path = sys._MEIPASS

        except Exception:
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, relative_path)

    def identifyTerm():
        currentTime = str(date.today())
        elements = currentTime.split("-")
        month = int(elements[1])
        if 8 < month <= 12:
            GB.CURRENTTERM = elements[0]+"01"
        elif 4 < month <= 8:
            GB.CURRENTTERM = str(int(elements[0])-1) + "03"
        else:
            GB.CURRENTTERM = str(int(elements[0])-1) + "02"


    def login(browser):
        unamePromt = browser.find_element(By.XPATH, '//*[@id="UserID"]')
        passPromt = browser.find_element(By.XPATH, '//*[@id="PIN"]')
        loginButton = browser.find_element(By.XPATH, '/html/body/div[3]/form/p/input')
        unamePromt.click()
        unamePromt.send_keys(GB.USERNAME)
        passPromt.click()
        passPromt.send_keys(GB.PASSWORD)
        loginButton.click()


    def enroll(browser):
        #head to student section
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/span/map/table/tbody/tr[1]/td/table/tbody/tr/td[3]/a'))).click()

        #open registration page
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/table[1]/tbody/tr[1]/td[2]/a'))).click()

        #**********************
        #select term
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/table[1]/tbody/tr[1]/td[2]/a'))).click()

        #wait until the term dropdown menu is clickable
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, 'term_id')))
        termDropdown = Select(browser.find_element(By.ID, 'term_id'))
        termDropdown.select_by_value(GB.CURRENTTERM)

        #submit changes
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form/input[2]'))).click()
        #**********************

        #selecting a term here may be optional, directly heading to the registration process may or may not show you confirmation for the term selection
        #possbily, it reads it from the cookies if any term is selected previously and gecko driver automated firefox does not contain cookies afaik
        #in order to bypass choosing term explicitly, you can comment out the lines between stars and have below line work
        #it is for clicking the submit button in case of a confirmation, when there is no such button, script will crash, use with care

        #submit the default term
        #WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form/input'))).click()

        #open add/drop page
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/table[1]/tbody/tr[2]/td[2]/a'))).click()

        #locate the first imput box
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form/table[3]/tbody/tr[2]/td[1]/input[2]')))
        for i, crn in enumerate(GB.CRNS):
            browser.find_element(By.XPATH, '/html/body/div[3]/form/table[3]/tbody/tr[2]/td[{}]/input[2]'.format(i+1)).send_keys(crn)
        browser.find_element(By.XPATH, '/html/body/div[3]/form/table[3]/tbody/tr[2]/td[{}]/input[2]'.format(len(GB.CRNS)-1)).send_keys(Keys.ENTER)


    def navigateToSchedule(browser):
        #head to student section
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/span/map/table/tbody/tr[1]/td/table/tbody/tr/td[3]/a'))).click()

        #open registration page
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/table[1]/tbody/tr[1]/td[2]/a'))).click()

        #select term
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/table[1]/tbody/tr[1]/td[2]/a'))).click()

        #wait until the term dropdown menu is clickable
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, 'term_id')))
        termDropdown = Select(browser.find_element(By.ID, 'term_id'))
        termDropdown.select_by_value(GB.CURRENTTERM)

        #submit changes
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form/input[2]'))).click()

        #open detailed schedule page
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/table[1]/tbody/tr[5]/td[2]/a'))).click()


    def checkUntilThereIsAvailableSeat(browser, CRN):
        browser.get(GB.SEATURL.format(GB.CURRENTTERM, CRN))
        remainingSeats = int(WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/table[1]/tbody/tr[2]/td/table/tbody/tr[2]/td[3]'))).text)
        while remainingSeats == 0:
            time.sleep(0.2)
            browser.get(GB.SEATURL.format(GB.CURRENTTERM, CRN))
            remainingSeats = int(WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/table[1]/tbody/tr[2]/td/table/tbody/tr[2]/td[3]'))).text)

