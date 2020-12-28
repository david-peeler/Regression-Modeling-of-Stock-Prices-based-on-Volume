from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

STOCK_TICKER = "plug"
csvFields = ["Date", "Open", "High", "Low", "Close", "Volume"]
fileName = STOCK_TICKER + ".csv"

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.set_headless(True)
driver = webdriver.Chrome(r'C:\Users\CS 2110\Desktop\Trader\Data Collection\Drivers\chromedriver.exe', chrome_options=options) 
driver.maximize_window()



with open(fileName, 'w', newline = '') as csvfile:
    filewriter = csv.writer(csvfile)
    filewriter.writerow(csvFields)
    print("created file called " + fileName)


    #Data starts Jan 1st, 1996
    day = 1
    year = 5
    months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    month = 7

    dataHolder = {}

    #if there is a table for the price/volume/whatever --> "/html/body/center/div[4]/table[2]/tbody/tr/td[4]/table[3]/tbody/tr/td[4]/span/select/option[" + str(month) + "]"
    #if there is not --> "/html/body/center/div[4]/table[2]/tbody/tr/td[4]/table[2]/tbody/tr/td[4]/span/select/option[" + str(month) + "]"


    #get main page and check if there is 
    driver.get("https://www.historicalstockprice.com/history/?a=historical&ticker=" + STOCK_TICKER + "&month=01&day=01&year=1996&x=9&y=10")
    while year < 26:
        #check for pop-up 
        try:
            driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div/div/div[2]/button[2]").click()
        except:
            print("no pop up detected")


        print("on url " + driver.current_url)

        try:
            driver.find_element_by_xpath("/html/body/center/div[4]/table[2]/tbody/tr/td[4]/table[3]/tbody/tr/td[4]/span/select/option[1]")
            is_there_data = True
        except NoSuchElementException:
            is_there_data = False

        if(not is_there_data):
            print(str(day) + " " + months[month - 1] + " " + str(year + 1995) + " - no data")
            driver.find_element_by_xpath("/html/body/center/div[4]/table[2]/tbody/tr/td[4]/table[2]/tbody/tr/td[4]/span/select/option[" + str(month) + "]").click()
            driver.find_element_by_xpath("/html/body/center/div[4]/table[2]/tbody/tr/td[4]/table[2]/tbody/tr/td[5]/span/select/option[" + str(day) + "]").click()
            driver.find_element_by_xpath("/html/body/center/div[4]/table[2]/tbody/tr/td[4]/table[2]/tbody/tr/td[6]/span/select/option[" + str(year) + "]").click()
            driver.find_element_by_xpath("/html/body/center/div[4]/table[2]/tbody/tr/td[4]/table[2]/tbody/tr/td[7]/input").click()

            print("got page for "+ str(day) + " " + months[month - 1] + " " + str(year + 1995) + " for ticker " + STOCK_TICKER + " - " + driver.current_url)
        else:
            try:
                driver.find_element_by_xpath("/html/body/center/div[4]/table[2]/tbody/tr/td[4]/table[3]/tbody/tr/td[4]/span/select/option[" + str(month) + "]").click()
                driver.find_element_by_xpath("/html/body/center/div[4]/table[2]/tbody/tr/td[4]/table[3]/tbody/tr/td[5]/span/select/option[" + str(day) + "]").click()
                driver.find_element_by_xpath("/html/body/center/div[4]/table[2]/tbody/tr/td[4]/table[3]/tbody/tr/td[6]/span/select/option[" + str(year) + "]").click()
                driver.find_element_by_xpath("/html/body/center/div[4]/table[2]/tbody/tr/td[4]/table[3]/tbody/tr/td[7]/input").click()
                

                temp = []
                for i in range(1, 7):
                    temp.append(driver.find_element_by_xpath("/html/body/center/div[4]/table[2]/tbody/tr/td[4]/table[2]/tbody/tr/td/table/tbody/tr[2]/td[" + str(i) + "]/font").text)

                filewriter.writerow(temp)
                print("wrote in data for " + str(day) + " " + months[month - 1] + " " + str(year + 1995) + " for ticker " + STOCK_TICKER)

            except:
                print("error occured")

        #increment day/month/yr
        day+=1
        if(day > 31):
            month+=1
            day = 1
            if(month == 13):
                day = 1
                month = 1
                year+=1
