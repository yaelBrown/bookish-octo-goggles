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

WEBSITES = []
API_URL = ""
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

def logInit():
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
    randomNum = random.randint(0,len(WEBSITES))
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

def main():
    # make requests to random websies
    # send random emails to random address
    # send a update to api
    logInit()

    update = {}
    update["hostname"] = HOSTNAME

    while True:
        actionWeb()
        update["webReq"] = 1
        updateOut = json.dumps(update)
        # print(updateOut)
        time.sleep(random.randint(1,10))

if __name__ == "__main__":
    main()




# test with backend make changes
# generate a config dictionary
# have the file read and configure to the config dictionary