import utilities as u
import rain as r
import eventlogger as e
import texting as t
import os
import dbconnections as db
import datetime


def main():
    u.initialize_log()
    e.add_events("PROGRAM START - Gather Current Weather Data")
    __location__ = u.get_local_file_path()
    config = u.read_json(os.path.join(__location__, 'config.json'))
    db.setupdbs(os.getenv('MYSQLHOST'),
                '3306',
                os.getenv('MYSQLUSER'),
                os.getenv('MYSQLPASS'))
    raincondition = r.raincondition()
    if raincondition != "":
        for recepient in config["RECEPIENTS"]["RAINALERTS"].split(","):
            t.send_message(recepient, raincondition)
    else:
        print("No rain conditions")
    u.remove_old_log_files("logs",30)
    e.close_log()
    db.close_dbs()

main()