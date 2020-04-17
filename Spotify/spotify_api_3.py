import sys
import requests
import base64  # 나의 client id 와 secret key 를 base64 형태로 인코딩해주는 패키지
import json
import logging
import pymysql
import csv

client_id = "ab567c2671e34f2ebf5e6acbcb6db44f"
client_secret = "ef7ee3b5900c40048bc142e88f112562"

host = 'data-engineering.c9ck0xgcwbcx.us-east-2.rds.amazonaws.com'
port = 3306
username = 'SJ'
database = 'production'
password = 'qhrtns12'


def main():

    try:
        # 커넥트
        conn = pymysql.connect(host, 
                                user=username,
                                passwd=password, 
                                db=database, 
                                port=port, 
                                use_unicode=True, 
                                charset='utf8')
        cursor = conn.cursor()

    except:
        logging.error('Could not connect to RDS')
        sys.exit(1)


    print('connect')


    headers = get_headers(client_id, client_secret)

    # Batch
    cursor.execute("SELECT id FROM artists")
    artists = []
    for (id, ) in cursor.fetchall():
        artists.append(id)

    # 50개씩 묶기
    artist_batch = [artists[i: i+50] for i in range(0, len(artists), 50)]

    artist_genres = []

    for i in artist_batch:
        # ids =  1234,2345,3456 이런식으로 , 로 붙이기 (string)
        ids = ','.join(i)
        URL = "https://api.spotify.com/v1/artists/?ids={}".format(ids)

        r= requests.get(URL, headers=headers)
        raw = json.loads(r.text)

        for artist in raw['artists']:
            for genre in artist['genres']:
                artist_genres.append(
                    {
                        'artist_id': artist['id'],
                        'genre': genre                    }
                )

    for data in artist_genres:
        print(data)
        insert_row(cursor, data, 'artist_genres')
        
        conn.commit()
        sys.exit(0)



def get_headers(clinet_id, client_secret):
    
    endpoint = "https://accounts.spotify.com/api/token"
    encoded = base64.b64encode("{}:{}".format(client_id, client_secret).encode('utf-8')).decode('ascii')

    headers = {
        "Authorization": "Basic {}".format(encoded)
    }

    payload = {
        "grant_type": "client_credentials"
    }

    r = requests.post(endpoint, data = payload, headers=headers)

    access_token = json.loads(r.text)['access_token']

    # API를 불러오기 위한 headers 내부에 access_token 넣어주기
    headers = {
        "Authorization": "Bearer {}".format(access_token)
    }
    
    return headers 


def insert_row(cursor, data, table):

    columns = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    key_placeholders = ', '.join(['{0}=%s'.format(k) for k in data.keys()])
    sql = "INSERT INTO %s ( %s ) VALUES ( %s ) ON DUPLICATE KEY UPDATE %s" % (table, columns, placeholders, key_placeholders)
    cursor.execute(sql, list(data.values())*2)  

if __name__ == '__main__':
    main()