# Whatsapp message sending bot
This project can be used to send personalized whatsapp messages to multiple contacts within a very short period of time. This app can be used on MacOS and windows.

## Requirements:
- File with contacts and variables like [number1.csv](https://github.com/pranv11/send-bulk-personalized-whatsapp/blob/main/number1.csv).
- A file with text message and variables x1, x2, x3 where ever you want to switch the variables like [message.txt](https://github.com/pranv11/send-bulk-personalized-whatsapp/blob/main/message.txt).

## MacOS
- Install python by opening terminal and typing <code>brew install python </code>.
- Once python is installed, install selenium <code>pip install selenium </code> or <code> pip3 install selenium </code> 
- install pip with <code>brew install pip3</code>) if you don't have it already.
- Create a folder where you will store all the files for this application.
- Get a copy of <code> send.py </code> and keep it in the folder that you made.
- Go to [chromedriver](https://chromedriver.chromium.org/downloads) and download the chrome driver according to your chrome version and OS. Extract The file in the same folder as the code.
- create files with contacts and the messages in the same folder as web driver.
- Once you have your contacts files and the message file in the computer, go to the terminal and type the following code:
- <code> cd path/of/the/directory/with/code </code>.
- <code> python3 send.py </code> or <code> python3 send.py </code>
- If you get an error saying '“chromedriver” can’t be opened because Apple cannot check it for malicious software' just run the follwing command:<code>xattr -d com.apple.quarantine chromedriver</code>
- These 2 lines of code will run the python code and then follow along with the questions that pop up.
- Remember to add the path of the files requested and not just the names.

