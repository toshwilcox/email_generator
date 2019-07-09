
"""this file accepts a csv file containing the columns with first and last name (in seperate columns) and the
company name, with this information this code will generate different possiblities of emails that a person could have

----example---
first: Tosh
last: Wilcox
company: Finitive

first, dot, last ------------ Tosh.Wilcox@Finitive.com
first, then last ------------ ToshWilcox@Finitive.com
first initial, last --------- TWilcox@Finitive.com
first initial, dot, last ---- T.Wilcox@Finitive.com
first name ------------------ Tosh@Finitive.com
fist, last initial ---------- ToshW@Finitive.com
last ------------------------ Wilcox@Finitive.com

fill in the info at the bottom of the page in the if name == main section.
"""
import pandas
import numpy as np
import string


class EmailGenerator():
    def __init__(self, file_path, csv_name, first_name_label, last_name_label, company_label, company_site, new_csv):
        self.path = file_path
        self.csv_name = csv_name
        self.first = first_name_label
        self.last = last_name_label
        self.company = company_label
        self.site = company_site
        self.new_csv = new_csv
        self.emails_list = []
        self.full_path = ''
        self.backslash = False

        self.com = []
        self.net = []


    def get_data(self):
        if self.path[(len(self.path)-1)] == '/':
            self.full_path = self.path + self.csv_name
            self.backslash = True
        else:
            self.full_path = self.path + '/' + self.csv_name

        data = pandas.read_csv(self.full_path, encoding='utf-8')


        first = [str(i) for i in np.asarray(data[self.first])]
        last = [str(i) for i in np.asarray(data[self.last])]
        company = [str(i) for i in np.asarray(data[self.company])]
        site = [str(i) for i in np.asarray(data[self.site])]


        self.data = np.column_stack((np.asarray(first), np.asarray(last), np.asarray(company), np.asarray(site)))

    """define the name types"""
    def type1(self, first, last):
        return first + '.' + last
    def type2(self, first, last):
        return first + last
    def type3(self, first, last):
        return first[0] + last
    def type4(self, first, last):
        return first[0] + '.' + last
    def type5(self, first, last):
        return first
    def type6(self, first, last):
        return last
    def type7(self, first, last):
        return first + last[0]
    def type8(self, first, last):
        return first[0] + last[0]
    def type9(self, first, last):
        return first[0] + '.' + last[0]

    """format the company name"""
    def at_co(self, company):
        # clean up the company name
        # get rid of puntuation.
        co = company.translate(str.maketrans('', '', string.punctuation))
        co = co.replace('LLC', '')
        co = co.replace('Inc', '')
        co = co.replace('USA', '')
        co = co.replace('Corporation', '')
        co = co.replace('Services', '')
        co = co.replace('Acceptance', '')
        co = co.replace('VA', '')
        co = co.replace(' ', '')
        return '@' + co + '.com'

    def web_site(self, website_url, company):
        if website_url == 'nan':
            return self.at_co(company=company)
        else:
            # should end in .com or .net and have look like https://www.website.com or https://website.com
            if 'com' in website_url.split('.')[-1]:
                # this is a .com website
                if 'www' in website_url:
                    print(website_url.split('.')[1] + '.com')
                else:
                    print(website_url.split('/')[2] + '.com')
            elif 'net' in website_url.split('.')[-1]:
                # this is a .net website
                if 'www' in website_url:
                    print(website_url.split('.')[1] + '.net')
                else:
                    print(website_url.split('/')[2] + '.net')


    def to_csv(self):
        # last check to get rid of unwanted spaces
        e = []
        for i in self.emails_list:
            holder = i[0].replace(' ', '')
            holder = holder.replace("'", "")
            holder = holder.replace(' ', '')
            e.append((holder, i[1], i[2]))

        df = pandas.DataFrame(np.asarray(e))

        if self.backslash:
            df.to_csv(self.path + self.new_csv)
        else:
            df.to_csv(self.path + '/' + self.new_csv)


    def controller(self):
        self.get_data()
        #print(self.data)
        for point in self.data:
            if point[0] == 'nan' or point[1] == 'nan' or point[2] == 'nan':
                # print("Insufficient Data, you are missing first, last, or company name")
                pass
            else:
                self.web_site(website_url=point[3], company=point[2])
                #self.emails_list.append((self.type1(point[0], point[1]) + self.web_site(website_url=point[3], company=point[2]), point[0] + ' ' + point[1],  point[2]))
                #self.emails_list.append((self.type2(point[0], point[1]) + self.web_site(website_url=point[3], company=point[2]), point[0] + ' ' + point[1],  point[2]))
                #self.emails_list.append((self.type3(point[0], point[1]) + self.web_site(website_url=point[3], company=point[2]), point[0] + ' ' + point[1],  point[2]))
                #self.emails_list.append((self.type4(point[0], point[1]) + self.web_site(website_url=point[3], company=point[2]), point[0] + ' ' + point[1],  point[2]))
                #self.emails_list.append((self.type5(point[0], point[1]) + self.web_site(website_url=point[3], company=point[2]), point[0] + ' ' + point[1],  point[2]))
                #self.emails_list.append((self.type6(point[0], point[1]) + self.web_site(website_url=point[3], company=point[2]), point[0] + ' ' + point[1],  point[2]))
                #self.emails_list.append((self.type7(point[0], point[1]) + self.web_site(website_url=point[3], company=point[2]), point[0] + ' ' + point[1],  point[2]))
                #self.emails_list.append((self.type8(point[0], point[1]) + self.web_site(website_url=point[3], company=point[2]), point[0] + ' ' + point[1],  point[2]))
                #self.emails_list.append((self.type9(point[0], point[1]) + self.web_site(website_url=point[3], company=point[2]), point[0] + ' ' + point[1],  point[2]))

        #self.to_csv()


if __name__ == '__main__':
    """Enter the path to where the csv is stored, the name of the csv, dont forget .csv at the end
    , the column name where the first names are stored, the column name for last names and company names
    , and the name of the new csv that will be saved in the same path with all of the new emails."""
    emails = EmailGenerator(file_path='C:/Users/ToshWilcox/Tosh-projects/email_checker', csv_name='auto_finance.csv',
                            first_name_label='First Name', last_name_label='Last Name',
                            company_label='Company Name', company_site='Company Website', new_csv='TEST_generated_emails.csv')
    emails.controller()

    # last time I used this I went in and took the company name out of the website and put it into a different column
    # for example if the website was https://www.autofinance.com then I added autofinance.com to the column, that way you
    # can just add @ or if there was not website just use the self.at_co function.  This will need to be changed so that
    # doesn't have to be done manually.


