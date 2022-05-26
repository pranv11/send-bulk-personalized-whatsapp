from selenium import webdriver
import csv
from selenium.webdriver.common.keys import Keys
import time


#asking input from user.
location_of_chromedriver = input("enter the path of chromedriver: ")
file_numbers = input("enter the name of the files with numbers: ")
msg = input("enter the message you want to send: ")

driver = webdriver.Chrome(executable_path= location_of_chromedriver)

file = open(file_numbers, "r")
csv_reader = csv.reader(file)
lists_from_csv = []
string_message= ""
numbers_from_csv = []
var1_from_csv = []
var2_from_csv = []
var3_from_csv = []

#assigning variables to arrays
try:
    for row in csv_reader:
        numbers_from_csv.append(row[0])
        var1_from_csv.append(row[1])
        var2_from_csv.append(row[2])
        var3_from_csv.append(row[3])
except:
    print("the csv file input is invalid")

#opening whatsapp
driver.get('https://web.whatsapp.com/')


input('press enter after scanning QR code')


#looping to change the variables according to the data provided.
for i in range(len(numbers_from_csv)):
    with open(msg) as f:
        message = f.read()
    x = message.replace("x1", var1_from_csv[i])
    y = x.replace("x2", var2_from_csv[i])
    z = y.replace("x3", var3_from_csv[i])


    try:

        user = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[1]/div/div/div[2]/div/div[2]')

        user.send_keys(numbers_from_csv[i])
        user.send_keys(Keys.RETURN)

        msg_box = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')


        msg_box.send_keys(z)
        time.sleep(1)

        msg_box.send_keys(Keys.RETURN)
    except:
        print(f"An error occurred in sending message to {i}")
            
