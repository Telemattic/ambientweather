import datetime
import json
import mysql.connector
import urllib3

def get_dateutc(s):

    dateutc = None
    try:
        x = json.loads(s)
        dateutc = x[0]['lastData']['dateutc']
    except:
        pass

    return dateutc

def poll_ambientweather(keys):

    http = urllib3.PoolManager()
    r = http.request('GET', 'https://rt.ambientweather.net/v1/devices', fields=keys)

    if r.status != 200:
        print(f"AmbientWeather WARNING - {r.status}")
        return 1

    curr = r.data

    dt_curr = get_dateutc(curr)
    if dt_curr is None:
        print(f"AmbientWeather WARNING - problem getting timestamp\n{curr}")
        return 1

    cnx = mysql.connector.connect(user='haversack', password='hypervigilance',
                                  host='localhost', database='haversack')

    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM `weather` ORDER BY `id` DESC LIMIT 1")

    prev = None
    for row in cursor:
        prev = row['json']
        
    cursor.close()

    dt_prev = get_dateutc(prev)
    if dt_prev is not None and dt_curr <= dt_prev:
        # print(f"AmbientWeather OK - data already up-to-date")
        return 0

    cursor = cnx.cursor()

    cursor.execute("INSERT INTO `weather` (`json`) values (%s)", (curr,))

    cnx.commit()
    cursor.close()
    cnx.close()

    return 0

def main():

    keys = {'applicationKey':'bcb7f64ea78543d9b8c5a71bd6eefdce7d414cfb0dcb4158966eda3bcf09b906',
            'apiKey':'7986cf7a4f194401b2b286c51ec04b8d5f19db7a3cfb4336a04034c670254b93'}

    ret = poll_ambientweather(keys)
    exit(ret)

if __name__ == '__main__':
    main()
