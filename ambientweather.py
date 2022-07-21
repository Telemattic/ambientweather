import mysql.connector
import urllib3

def poll_ambientweather(keys):

    http = urllib3.PoolManager()
    r = http.request('GET', 'https://rt.ambientweather.net/v1/devices', fields=keys)

    if r.status != 200:
        print(f"AmbientWeather WARNING - {r.status}")
        return 1

    x = r.body.str()

    cnx = mysql.connector.connect(user='haversack', password='hypervigilance',
                                  host='localhost', database='haversack')
    cursor = cnx.cursor()

    cursor.execute("INSERT INTO `weather` (`json`) values (%s)", (x,))

    cnx.commit()
    cursor.close()
    cnx.close()

    return 0

def main():

    keys = {'applicationKey':'bcb7f64ea78543d9b8c5a71bd6eefdce7d414cfb0dcb4158966eda3bcf09b906',
            'apiKey':'7986cf7a4f194401b2b286c51ec04b8d5f19db7a3cfb4336a04034c670254b93'}

    poll_ambientweather(keys)
    exit(0)

if __name__ == '__main__':
    main()
