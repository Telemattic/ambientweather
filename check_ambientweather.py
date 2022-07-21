import datetime
import mysql.connector

def check_haversack():

    ts = datetime.datetime.now()

    cnx = mysql.connector.connect(user='haversack', password='hypervigilance',
                                  host='localhost', database='haversack')

    cursor = cnx.cursor()

    cursor.execute("SELECT `time` FROM `weather` ORDER BY `id` DESC LIMIT 1")
    for row in cursor:
        dt = row[0]
        
    cursor.close()
    cnx.close()

    delta = (datetime.datetime.now() - dt).total_seconds()

    interval = 300
    (status, ret) = ('OK', 0) if delta < interval * 2 else ('WARNING', 1)
    print(f"AmbientWeather {status} - last {dt.isoformat()} ({delta:.0f}s)")

    return ret

def main():

    ret = 2
    try:
        ret = check_haversack()
    except Exception as err:
        print(f"AmbientWeather CRITICAL - exception caught {err=} {type(err)=}")
        
    exit(ret)

if __name__ == '__main__':
    main()

        
