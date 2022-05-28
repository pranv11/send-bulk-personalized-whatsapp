from logging import exception
import platform
import random
from selenium import webdriver
import csv
from selenium.webdriver.common.by   import By
from selenium.webdriver.common.keys import Keys
import time
import os.path
import subprocess

#
# get current directory per OS
#
OSname=platform.system()
if OSname=="Darwin" or OSname=="Linux": # MacOS/Unix
    pwd=subprocess.getoutput('pwd')
elif OSname=="Windows":
    pwd=subprocess.getoutput('cd') 

#
# validate existence of chromedriver
#
default_file_chromedriver = pwd + '/chromedriver'
file_chromedriver = input("Enter the full path of the chromedriver file [./chromedriver]: ")
if file_chromedriver=="": file_chromedriver=default_file_chromedriver
try:
    file_exists=os.path.exists(file_chromedriver)
    if file_exists == False: raise exception
except:
    print ("File does not exist "+file_chromedriver)
    exit(1)

#
# validate existence of numbers file
#
default_file_numbers= pwd + '/numbers.csv'
file_numbers = input("Enter the name of the files with numbers [./numbers.csv]: ")
if file_numbers=="": file_numbers=default_file_numbers
try:
    file_exists=os.path.exists(file_numbers)
    if file_exists == False: raise exception
except:
    print ("File does not exist "+file_numbers)
    exit(1)

#
# validate existence of message file
#
default_file_msg= pwd + '/message.txt'
file_msg = input("Enter the name of the message file [./message.txt]: ")
if file_msg=="": file_msg=default_file_msg
try:
    file_exists=os.path.exists(file_msg)
    if file_exists == False: raise exception
except:
    print ("File does not exist "+file_msg)
    exit(1)

#
# read numbers file into arrays
#
whatsappnumber_from_csv = []
var1_from_csv = []
var2_from_csv = []
var3_from_csv = []

try:
    file = open(file_numbers, 'r')
    csv_reader = csv.reader(file)
    print('opened numbers file')
    for row in csv_reader:
        print (row)
        whatsappnumber_from_csv.append(row[0])
        var1_from_csv.append(row[1])
        var2_from_csv.append(row[2])
        var3_from_csv.append(row[3])
except:
    print("The numbers csv file input is invalid")
    exit(1)

file.close()

#
# prepare whatsapp window
#
driver = webdriver.Chrome(executable_path= file_chromedriver)
driver.get('https://web.whatsapp.com/')

input('Press enter after scanning QR code')

#
# read the message into a variable 
#
with open(file_msg, 'r') as file:
   message = file.read()

#
# Loop through each whatsapp number and substitute the variable values into the message tokens
#
for i in range(len(whatsappnumber_from_csv)):
    x = message.replace("x1", var1_from_csv[i])
    y = x.replace("x2", var2_from_csv[i])
    z = y.replace("x3", var3_from_csv[i])

    try:
        print ('Sending message ' + z + ' to ' + whatsappnumber_from_csv[i])
        #
        # Enter the Whatsapp number into the chrome window
        #
        user = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div[3]/div/div[1]/div/div/div[2]/div/div[2]')
        #print ('after find element whatsapp #')
        user.send_keys(whatsappnumber_from_csv[i])
        #print ('after send_keys whatsapp #')
        user.send_keys(Keys.RETURN)
        #print ('after send_keys return')
        #
        # Enter the message with substituted tokens into the chrome window
        #
        msg_box = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]')
        #print ('after find element message')
        msg_box.send_keys(z)
        #print ('after send keys message')
        msg_box.send_keys(Keys.RETURN)
        #print ('after send keys return')
        #
        # wait for a bit before the next message
        #
        time.sleep(random.randint(1,4))
        print ('Message sent successfully for ' + whatsappnumber_from_csv[i])
    except:
        print ('error raised while sending message for ' + whatsappnumber_from_csv[i])
driver.close()