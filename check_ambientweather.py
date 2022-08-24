import datetime
import json
import mysql.connector

def check_ambientweather():

    ts = datetime.datetime.now()

    cnx = mysql.connector.connect(user='haversack', password='hypervigilance',
                                  host='localhost', database='haversack')

    cursor = cnx.cursor()

    cursor.execute("SELECT `json` FROM `weather` ORDER BY `id` DESC LIMIT 1")

    curr = None
    for row in cursor:
        curr = row[0]
        
    cursor.close()
    cnx.close()

    try:
        curr = json.loads(curr)[0]['lastData']
    except:
        curr = None

    if curr is None:
        print("AmbientWeather CRITICAL - can't parse most recent data")
        return 2

    dt = curr['date'].replace('Z', '+00:00')
    dt = datetime.datetime.fromisoformat(dt)

    delta = (datetime.datetime.now(datetime.timezone.utc) - dt).total_seconds()
    details = f"{curr['tempf']:.1f}F / {curr['tempinf']:.1f}F"

    interval = 60
    (status, ret) = ('OK', 0) if delta < interval * 3 else ('WARNING', 1)
    print(f"AmbientWeather {status} - last {dt.astimezone().isoformat()} ({delta:.0f}s) - {details}")

    return ret

def main():

    ret = 2
    try:
        ret = check_ambientweather()
    except Exception as err:
        print(f"AmbientWeather CRITICAL - exception caught {err=} {type(err)=}")
        
    exit(ret)

if __name__ == '__main__':
    main()

        
