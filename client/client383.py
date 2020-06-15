import requests
import csv
import random
import time
import json
import socket
import smtplib
import platform

from datetime import datetime

from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

with open('config.json', 'r') as j:
    d = j.read()
    d = json.loads(d)

WEBSITES = []
API_URL = f"http://{d["hostname"]}:5000/update"
HOSTNAME = socket.gethostname()
WEIGHT = []
EMAIL_TO = ""
EMAIL_AUTHOR = ""
EMAIL_SERVER = ""
EMAIL_SUBJECT = f"Email from {HOSTNAME}"
EMAIL_BODY = f"Email from {HOSTNAME}"
OS = platform.platform()
LOG_TITLE = f"{HOSTNAME}-{OS}-client.log"

# Read websites.csv file
with open('websites.csv', newline='') as csvfile:
    temp = csv.DictReader(csvfile, delimiter=',')    
    for row in temp:
        WEBSITES.append(row["Root Domain"])

def config():
    # used to read config file and setup configuration
    pass

def logInit():
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
        print(f"Unable to read banner.txt: {e}")
    finally:
        b.close()

    # Initialize log
    now = datetime.now()
    with open(f'{LOG_TITLE}', 'w') as log:
        initStr = f"Castle Network Generator (CNG) Startup\n==========\nInitialized at {now}\nAPI_URL: {API_URL}\nHOSTNAME: {HOSTNAME}\nHOST OS: {OS}\nLOG_TITLE: {LOG_TITLE}\nWEIGHT: {WEIGHT}\nEMAIL_TO: {EMAIL_TO}\nEMAIL_AUTHOR: {EMAIL_AUTHOR}\nEMAIL_SERVER: {EMAIL_SERVER}\nEMAIL_SUBJECT: {EMAIL_SUBJECT}\nEMAIL_BODY: {EMAIL_BODY}\n==========\n\n"
        print("\n")
        print(initStr)
        log.write(initStr)
        log.close()
        
def log(s): 
    now = datetime.now()
    dt = now.strftime("%m/%d/%Y %H:%M:%S")
    print(f"CNG: {dt} {s}")
    with open(f'{LOG_TITLE}', 'a+') as log:
        log.write(f"CNG: {dt} {s}\n")

def actionWeb():
    randomNum = random.randint(0,(len(WEBSITES)-1))
    try: 
        r = requests.get(f"http://{WEBSITES[randomNum]}")
        log(f"Visiting http://{WEBSITES[randomNum]}")
    except Exception as e: 
        log(f"Error!!! visiting http://{WEBSITES[randomNum]}: {e}")

def actionEmail():
    # Not yet tested
    msg = MIMEMultipart()
    msg['From'] = EMAIL_AUTHOR
    msg['To'] = EMAIL_TO
    msg['Subject'] = EMAIL_SUBJECT

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()

def sendUpdate(j):
    # used to send updates to server
    updateCnt = 0
    if updateCnt == 0:
        try: 
            requests.post(API_URL, json=j)
            log(f"Sending update to API\n\tAPI_URL: {API_URL}\n\tDATA: {j}")
            updateCnt += 1
        except Exception as e:
            log(f"Error !!! unable to send update to {API_URL}, Error: {e}")
    else:
        requests.put(API_URL, data=j)
        try:
            log(f"Sending update to API\n\tAPI_URL: {API_URL}\n\tDATA: {j}")
        except Exception as e:
            log(f"Error !!! unable to send update to {API_URL}, Error: {e}")

def main():
    # make requests to random websies
    # send random emails to random address
    # send a update to api
    logInit()

    update = {}
    update["hostname"] = HOSTNAME
    update["OS"] = OS
    update["webReq"] = 0
    update["email"] = 0

    actionCnt = 0
    updateCnt = 0

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



# test with backend make changes
# generate a config dictionary
# have the file read and configure to the config dictionary