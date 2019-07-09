from selenium import webdriver
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import pandas
import numpy as np
import time
import datetime
import sqlite3 as sql
import requests
import time
from selenium.webdriver.common.by import By
import random
# get the email sender from the linkedin_scrape folder
import sys

sys.path.insert(0, 'C:/Users/ToshWilcox/Tosh-projects/linkedin_scrape')

import email_sender
import datetime


class EmailCheck():
    def __init__(self, path, csv_name, new_csv, update):
        self.path = path
        self.csv_name = csv_name
        self.new = new_csv
        self.full_path = ''
        self.backslash = False
        self.site = "http://mailtester.com"
        self.email_list = []
        self.valid_list = []
        self.not_valid_list = []
        self.try_again = []
        self.update = update
        #self.writer = pd.ExcelWriter('valid.xlsx', engine='xlsxwriter')
        # set up the web driver.
        # the google webdriver must be downloaded and put into the file named below
        chrome_path = r"C:\Users\ToshWilcox\Tosh-projects\ABL_scrape\chromedriver.exe"
        self.driver = webdriver.Chrome(chrome_path)
        self.response = requests.get(self.site)


    def openPage(self):
        self.driver.get(self.site)

    def set_email(self, email):
        email_box = self.driver.find_element_by_name('email')
        email_box.clear()
        email_box.send_keys(email)

    def check_validity(self, email):
        soup = BeautifulSoup(self.driver.page_source, features='lxml')
        text = soup.findAll(text=True)

        for t in text:
            if t == 'E-mail address is valid':
                print("\n", email, " IS A VALID EMAIL ADDRESS!\n")
                return 0
            if t == "The domain is invalid or no mail server was found for it.":
                print('\n', email , ' IS NOT A VALID DOMAIN, CHECK THIS\n')
                return 1
            if t == "Unknown response from mail server (status code: 450)":
                print('\n', 'THE SERVER IS NOT WORKING, TRY AGAIN LATER FOR', email, '\n')
                return 2
            if t == "E-mail address does not exist on this server":
                print("dne")
                return 3
            if t == "Server doesn't allow e-mail address verification":
                print("not allowed")
                return 4
            if t == "Unknown response from mail server (status code: 503)":
                print("no responce")
                return 5
            else:
                pass

    def get_list(self, csv):
        if self.path[(len(self.path)-1)] == '/':
            self.full_path = self.path + csv
            self.backslash = True
        else:
            self.full_path = self.path + '/' + csv

        data = pandas.read_csv(self.full_path, encoding='utf-8')
        e_ = np.asarray(data['Email'])
        n_ = np.asarray(data['Name'])
        c_ = np.asarray(data['Company'])

        return np.column_stack((e_, n_, c_))

    def pause(self):
        num = random.randint(2,4)
        time.sleep(num)
        self.driver.implicitly_wait(num)

    def click_submit(self):
        self.driver.find_element_by_xpath('//*[@id="content"]/form/table/tbody/tr[2]/td/input').click()


    def controller(self):
        # this is where everything will be done from
        # step one open the page.

        self.openPage()
        self.pause()
        possibilities = self.get_list(self.csv_name)

        if self.update:
            current = self.get_list(self.new)
            for email in current:
                self.valid_list.append((email[0], email[1], email[2]))
                # gets all of the current values into the list that we will work with.

            # figures out what is the last valid email that we have, then we will start from that point
            for i in range(len(possibilities)):
                if np.all(current[len(current)-1] == possibilities[i]):
                    checked_ind = i + 1
                    # that is plus two on excel, starts at 1 and the title.
            for i in range(len(possibilities)):
                if i < checked_ind:
                    pass
                    # already have this email checked.
                else:
                    self.set_email(possibilities[i][0])
                    self.pause()
                    self.click_submit()
                    self.pause()
                    check = self.check_validity(possibilities[i][0])
                    if check == 0:
                        # if the email is valid then put it in the list
                        self.valid_list.append((possibilities[i][0],  possibilities[i][1], possibilities[i][2]))
                        print("\n", possibilities[i], " IS A VALID EMAIL ADDRESS!\n")
                    elif check == 2:
                        self.try_again.append((possibilities[i][0],  possibilities[i][1], possibilities[i][2]))
                    else:
                        pass

                    df = pandas.DataFrame(np.asarray(self.valid_list), columns=['Email', 'Name', 'Company'])
                    if self.backslash:

                        df.to_csv(self.path + self.new)
                    else:
                        df.to_csv(self.path + '/' + self.new)
                    self.pause()




        else:

            for email in possibilities:
                self.set_email(email[0])
                self.pause()
                self.click_submit()
                self.pause()
                check = self.check_validity(email[0])
                if check == 0:
                    # if the email is valid then put it in the list
                    self.valid_list.append((email[0], email[1], email[2]))
                    print("\n", email, " IS A VALID EMAIL ADDRESS!\n")
                elif check == 2:
                    self.try_again.append((email[0], email[1], email[2]))
                else:
                    pass

                df = pandas.DataFrame(np.asarray(self.valid_list))
                if self.backslash:

                    df.to_csv(self.path + self.new)
                else:
                    df.to_csv(self.path + '/' + self.new)
                self.pause()


if __name__ == '__main__':

    try:

        abl = EmailCheck(path='C:/Users/ToshWilcox/Tosh-projects/email_checker', csv_name='generated_emails.csv',
                     new_csv='valid.csv', update=False)
        abl.controller()
    except:
        sub = 'Error in email_checker.py python script'
        mes = 'There was an error in the email_checker script,\n\n This occured at ' + str(datetime.datetime.now()) + \
                '\n\n Please check the script and the server to make sure everything is working, then continure running.'
        email_sender.send_email(sub, mes, 'tosh@finitive.com')



