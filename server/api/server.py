import psycopg2
import json
import socket
import platform
import time

from flask import Flask, request, render_template
from flask_cors import CORS
from datetime import datetime
from configparser import ConfigParser

"""
Example 'reporting_machines' dictionary
    'reporting_machine': {
        'hostname': '',
        'last_update': ''
    }

    hostname - name of machine
    last_update - Date/Time of last update
"""

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

overview = {
    'npcs': {
        'windows': 0,
        'linux': 0,
        'macOS': 0
    },
    'activities': {
        'web': 0,
        'email': 0
    },
    'reporting_machines': []
}

HOSTNAME = socket.gethostname()
OS = platform.platform()
LOG_TITLE = f"{HOSTNAME}-{OS}-server.log"

def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

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
        print(f"Unable to read banner.txt: {e}")
    finally:
        b.close()

def logInit():
    # Initialize a cheeky banner
    # try: 
    #     with open("banner.txt") as b:
    #         line = b.readline()
    #         cnt = 1
    #         while line:
    #             print(line.strip())
    #             line = b.readline()
    #             cnt += 1
    # except Exception as e: 
    #     print(f"Unable to read banner.txt: {e}")
    # finally:
    #     b.close()

    # Initialize log
    now = datetime.now()
    try: 
        with open(f"{LOG_TITLE}", "w") as log:
            initStr = f"Castle Network Generator (CNG) Server Startup\n==========\nInitialized at {now}\nHostname: {HOSTNAME}\nOS: {OS}\nLOG_TITLE: {LOG_TITLE}"
            print(initStr)
            print(overview)
            log.write(f"{initStr}\n{overview}\n")
    except Exception as e: 
        print(f"Error initializing log: {e}")
    finally:
        log.close()


def log(s):
    now = datetime.now()
    dt = now.strftime("%m/%d/%Y %H:%M:%S")
    print(f"CNG-S: {dt} {s}")
    with open(f'{LOG_TITLE}', 'a+') as log:
        log.write(f"CNG-S: {dt} {s}\n")

def connect(): 
    conn = None
    try: 
        params = config()
        
        log("DB: Connecting to the PostgresSQL database...")
        
        conn = psycopg2.connect(**params)
        return conn.cursor()
    except (Exception, psycopg2.DatabaseError) as e:
        log(f"DB: Error: {e}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/update", methods=["POST", "PUT"])
def update():
    try:
        data = request.get_json(force=True)
        
        overview["activities"]["web"] += data["webReq"]
        overview["activities"]["email"] += data["email"]

        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y %H:%M:%S")
        
        id = len(overview["reporting_machines"])
        
        hn = data["hostname"]

        log(f"Recieved update from {hn}")

        try:
            for h in overview["reporting_machines"]:
                if data["hostname"] in h["hostname"]:
                    result = h
            log(f"result: {result}")
            idx = result["id"]
            overview["reporting_machines"][idx]["last_update"] = date_time
        except: 
            if "windows" in data["OS"]:
                overview["npcs"]["windows"] += 1
            elif "Linux" in data["OS"]:
                overview["npcs"]["linux"] += 1
            elif "macOS" in data["OS"]:
                overview["npcs"]["macOS"] += 1
            else:
                # add log for unable to indentify OS
                pass
            temp = {"id": id, "hostname": data["hostname"], "last_update": date_time, "OS": data["OS"]}
            log(f"DB: adding to db: {temp}")
            overview["reporting_machines"].append(temp)    

        cur = connect()
        try:
            npcsSQL = json.dumps(overview["npcs"])
            activitiesSQL = json.dumps(overview["activities"])
            reporting_machinesSQL = json.dumps(overview["reporting_machines"])
            sql = f"INSERT INTO overview (id, npcs, activities, reporting_machines) values ('{id}', '{npcsSQL}', '{activitiesSQL}', '{reporting_machinesSQL}')"         
            cur.execute(sql)
            log("DB: added to db")
        except Exception as e:
            log(f"DB: error adding to db: {e}")
        finally:
            if cur is not None:
                cur.close()
                log('DB: Database connection closed.')
                log(str(overview))
        
        log(overview)

        return {"msg": "update recieved", "overview": overview}, 200
    except Exception as e:
        print("hostname was not found in request")
        return {"msg": "error with update", "error": f"{e}"}, 418

@app.route("/status", methods=["GET"])
def status():
    if overview["npcs"]["windows"] == 0 and overview["npcs"]["linux"] == 0 and overview["npcs"]["macOS"] == 0:
        log("DB: getting some data from db")

    return overview, 200

if __name__ == "__main__":
    logInit()
    banner()
    app.run(debug=True)





# convert python json to postgres array. 