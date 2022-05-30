from logging import exception
import os
import platform
import random
import sys
from selenium import webdriver
import csv
from selenium.webdriver.common.by   import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import subprocess
import argparse


print('')
print("make sure you format the csv file if downloaded from Google sheets")
print("dos2unix contacts.csv")
print("awk -F',' '{split($1,a,' '); print $2, a[1]}' contacts.csv")
print('')

#
# parse arguments of the main program
#
try:
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('-n', '--numbersfile', default='numbers.csv', help='the file containing whatsapp numbers, personalized token values')
    my_parser.add_argument('-m', '--messagefile', default='message.txt', help='the file containing whatsapp message, personalized tokens')
    my_parser.add_argument('-d', '--chromedriver', default='chromedriver', help='the full path for chromedriver including directory')
   
    args = my_parser.parse_args()

    if os.path.exists(args.numbersfile) == False: 
        print ('Numbersfile does not exist')
        sys.exit(1)
    else:
        file_numbers=args.numbersfile
    
    if os.path.exists(args.messagefile) == False: 
        print ('Messagefile does not exist')
        sys.exit(1)
    else:
        file_msg=args.messagefile

    #
    # get current directory per OS
    #
    OSname=platform.system()
    if OSname=="Darwin" or OSname=="Linux": # MacOS/Unix
        pwd=subprocess.getoutput('pwd')
        delim='/'
    elif OSname=="Windows":
        pwd=subprocess.getoutput('cd') 
        delim='\\'
    #
    # construct the full path to chromedriver
    #
    file_chromedriver = pwd + delim + args.chromedriver

    if os.path.exists(file_chromedriver) == False: 
        print ('Chromedriver does not exist')
        sys.exit(1)

except:
    print('Error in argument parsing')
    sys.exit(1)

print('Numbers file is ' + file_numbers)
print('Message file is ' + file_msg)
print('Chromedriver file is ' + file_chromedriver)

#
# Read numbers and personalized token values into arrays
# This program assumes max of 3 tokens that will be substitited
# 
whatsappnumber_from_csv = []
var1_from_csv = []
var2_from_csv = []
var3_from_csv = []

#
# function to see if an index exists for an array or not
#
def index_exists(ls, i):
    return (0 <= i < len(ls))

#
# function to sanitize whatsapp no so that we don't get invalid number error
#
def sanitize(numstring):
    newnumber=numstring.replace("(", "")
    newnumber=newnumber.replace(")", "")
    newnumber=newnumber.replace("-", "")
    newnumber=newnumber.replace(" ", "")
    # if country code not given, default to +1 for US
    if len(newnumber)==10: newnumber="+1"+newnumber
    return newnumber

try:
    file = open(file_numbers, 'r')
    csv_reader = csv.reader(file)
    for row in csv_reader:
        #print (row)
        sanitized_whatsapp_no = sanitize(row[0])
        whatsappnumber_from_csv.append(sanitized_whatsapp_no)
        if index_exists(row, 1): var1_from_csv.append(row[1]); #print('added var1')
        if index_exists(row, 2): var2_from_csv.append(row[2]); #print('added var2')
        if index_exists(row, 3): var3_from_csv.append(row[3]); #print('added var3')
except:
    print("The numbers csv file input is invalid")
    exit(1)

file.close()

#
# prepare whatsapp window
#
options = Options();
if OSname=="Darwin" or OSname=="Linux": # MacOS/Unix
    options.add_argument("user-data-dir=/tmp/whatsapp")
elif OSname=="Windows": #Windows
    options.add_argument("user-data-dir=" + os.environ['USERPROFILE'] + "\\AppData\\Local\\Google\\Chrome\\User Data") 

driver = webdriver.Chrome(executable_path= file_chromedriver, options=options)

#
# read the message into a variable 
#
with open(file_msg, 'r') as file:
   message = file.read()

#
# Loop through each whatsapp number and substitute the variable values into the message tokens
#
for i in range(len(whatsappnumber_from_csv)):
    if index_exists(var1_from_csv, i): new_message = message.replace("x1", var1_from_csv[i])
    if index_exists(var2_from_csv, i): new_message = new_message.replace("x2", var2_from_csv[i])
    if index_exists(var3_from_csv, i): new_message = new_message.replace("x3", var3_from_csv[i])

    try:
        print ('Sending message ' + new_message + ' to ' + whatsappnumber_from_csv[i])
        #
        # Open whatsapp web window for the contact. You don't need to save this contact in the phone.
        #
        driver.get('https://web.whatsapp.com/send/?phone=' + whatsappnumber_from_csv[i])
        #
        # only wait for the QR code authentication the first time, after that it will remember from cache
        # If the QR code authentication was done in the earlier session, even this is not needed, but it's necessary to have this step 
        # to make sure the authentication is successful
        #
        if i==0: input('\n\nPress enter after scanning QR code')

        #
        # wait for the page to load, it can take a while sometimes
        #
        time.sleep(7)
        #
        # Enter the message with substituted tokens into the chrome window
        # The xpath value will keep changing as whatsapp evolves. It has to be tested once in a while.
        # To get the correct value, click on the text field in browser and right click inspect
        # then right ckck on the inspection element and copy full xpath here
        # 
        msg_box = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]')
        #print ('after find element message')
        msg_box.send_keys(new_message)
        #print ('after send keys message')
        msg_box.send_keys(Keys.RETURN)
        #print ('after send keys return')
        #
        # wait for a bit before the next message
        #
        time.sleep(random.randint(1,4))
        print ('Message sent successfully for ' + whatsappnumber_from_csv[i])
    except:
        print ('Error raised while sending message for ' + whatsappnumber_from_csv[i])
driver.quit()