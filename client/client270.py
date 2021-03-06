import requests
import csv
import random
import time
import json
import socket
import smtplib
import platform
​
from datetime import datetime
​
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
​
WEBSITES = []
API_IP = "192.168.1.203"
API_VARS = "http://" + API_IP + ":5000/var"
API_URL = "http://" + API_IP + ":5000/update"
HOSTNAME = socket.gethostname()
WEIGHT = []
EMAIL_TO = ""
EMAIL_AUTHOR = ""
EMAIL_SERVER = ""
EMAIL_SUBJECT = "Email from {}".format(HOSTNAME)
EMAIL_BODY = "Email from {}".format(HOSTNAME)
OS = platform.platform()
LOG_TITLE = "{}-{}-client.log".format(HOSTNAME, OS)
​
# Read websites.csv file
with open('websites.csv') as csvfile:
    temp = csv.DictReader(csvfile, delimiter=',')    
    for row in temp:
        WEBSITES.append(row["Root Domain"])
​
def banner():
    # Initialize a cheeky banner
    try: 
        with open("banner.txt") as b:
            line = b.readline()
            cnt = 1
            while line:
                print(line.strip())
                line = b.readline()
                cnt += 1
    except Exception as e: 
        print("Unable to read banner.txt: {}".format(e))
    finally:
        b.close()
​
def logInit():
    banner()
​
    # Initialize log
    now = datetime.now()
    with open('{}'.format(LOG_TITLE), 'w') as log:
        initStr = "Castle Network Generator (CNG) Startup\n==========\nInitialized at {}\nAPI_IP: {}\nAPI_VARS: {}\nAPI_URL: {}\nHOSTNAME: {}\nHOST OS: {}\nLOG_TITLE: {}\nWEIGHT: {}\nEMAIL_TO: {}\nEMAIL_AUTHOR: {}\nEMAIL_SERVER: {}\nEMAIL_SUBJECT: {}\nEMAIL_BODY: {}\n==========\n\n".format(now, API_IP, API_VARS, API_URL, HOSTNAME, OS, LOG_TITLE, WEIGHT, EMAIL_TO, EMAIL_AUTHOR, EMAIL_SERVER, EMAIL_SUBJECT, EMAIL_BODY)
        print("\n")
        print(initStr)
        log.write(initStr)
        log.close()
        
def log(s): 
    now = datetime.now()
    dt = now.strftime("%m/%d/%Y %H:%M:%S")
    print("CNG: {} {}".format(dt,s))
    with open("{}".format(LOG_TITLE), 'a+') as log:
        log.write("CNG: {} {}".format(dt,s))
​
def actionWeb():
    randomNum = random.randint(0,(len(WEBSITES)-1))
    try: 
        r = requests.get("http://{}".format(WEBSITES[randomNum]))
        log("Visiting http://{}".format(WEBSITES[randomNum]))
    except Exception as e: 
        log("ERROR!!! Visiting http://{}: {}".format(WEBSITES[randomNum], e))
​
def actionEmail():
    # Not yet tested
    msg = MIMEMultipart()
    msg['From'] = EMAIL_AUTHOR
    msg['To'] = EMAIL_TO
    msg['Subject'] = EMAIL_SUBJECT
​
    msg.attach(MIMEText(message, 'plain'))
​
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()
​
def sendUpdate(j):
    # used to send updates to server
    updateCnt = 0
    if updateCnt == 0:
        try: 
            requests.post(API_URL, json=json.dumps(j))
            log("Sending update to API\n\tAPI_URL: {}\n\tDATA: {}".format(API_URL, j))
            updateCnt += 1
        except Exception as e:
            log("Error !!! unable to send update to {}, Error: {}".format(API_URL, e))
    else:
        requests.put(API_URL, data=j)
        try:
            log("Sending update to API\n\tAPI_URL: {}\n\tDATA: {}".format(API_URL, j))
        except Exception as e:
            log("Error !!! unable to send update to {}, Error: {}".format(API_URL, e))
​
def getVars():
    try: 
        out = requests.get(API_VARS)
        out = out.json()
        log("Variables: Getting variables from server: {}".format(out))
        return out
    except Exception as e: 
        log("Variables: Error getting variables from server: {}".format(e))
​
def assignVars():
    pass
​
def main():
    # make requests to random websies
    # send random emails to random address
    # send a update to api
    logInit()
​
    VARS = {}
    while VARS == {}:
        try: 
            VARS = getVars()
        except Exception as e:
            log("Variables: Error saving Variables: {}".format(e))
​
    print("\n")
​
    update = {}
    update["hostname"] = HOSTNAME
    update["OS"] = OS
    update["webReq"] = 0
    update["email"] = 0
​
    actionCnt = 0
    updateCnt = 0
​
    while True:
        actionWeb()
        update["webReq"] += 1
        actionCnt += 1
        # print(updateOut)
        if actionCnt % 5 == 0:
            sendUpdate(update)
            update["webReq"] = 0
            update["email"] = 0
            actionCnt = 0
        time.sleep(random.randint(1,10))
        
if __name__ == "__main__":
    main()
    # 6.25.2020