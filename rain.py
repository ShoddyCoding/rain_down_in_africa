import dbconnections as db
import eventlogger as er
import os

def raincondition():
    """grab rainfall in past 48 hours, return blank string if none"""
    rainfall = ""
    try:
        query = """select truncate(sum(t1.rain)/25.4,2)  as rain_total
                FROM ( SELECT FROM_UNIXTIME(dt) as date_time
                , (rain * 1) as rain from weather.weather_history
                where from_unixtime(dt) < now() order by dt desc LIMIT 48 ) as t1"""
        db.conn_local_prod_cursor.execute(query)
        amount = db.conn_local_prod_cursor.fetchall()
        if amount[0][0] > 0.1 and amount[0][0] != 'None':
            rainfall = "In the past 48 hours, we've had {0} inches of rainfall".format(amount[0][0])
    except Exception as e:
        er.add_events("ERROR: Issue pulling past 2 days of rainfall: {}".format(e))
    return rainfall

if __name__ == "__main__":
    db.setupdbs(os.getenv('MYSQLHOST'),
                '3306',
                os.getenv('MYSQLUSER'),
                os.getenv('MYSQLPASS'))
    a = raincondition()
    print(a)