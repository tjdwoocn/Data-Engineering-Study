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
password = ''


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

    # Spotify Search API
    params = {
        "q": "BTS",
        "type": "artist",
        "limit": "1", 
    }
    
    r = requests.get("https://api.spotify.com/v1/search", params = params, headers=headers)
    raw = json.loads(r.text)
    print(raw['artists'].keys())

    print(raw['artists']['items'][0].keys())

    artist_raw = raw['artists']['items'][0]

    artist = {}

    # 가수의 정보가 BTS가 맞다면
    if artist_raw['name'] == params['q']:
        artist.update(
            {
                'id': artist_raw['id'],
                'name': artist_raw['name'],
                'followers': artist_raw['followers']['total'],
                'popularity': artist_raw['popularity'],
                'url': artist_raw['external_urls']['spotify'],
                'image_url': artist_raw['images'][0]['url'],
            }
        )

    insert_row(cursor, artist, 'artists')
    conn.commit()

    sys.exit(0)


    raw = json.loads(r.text)

    total = raw['total']
    offset = raw['offset']
    limit = raw['limit']
    next = raw['next']

    albums = []
    albums.extend(raw['items'])

    # 최대 100개만 뽑아 오겠다
    count = 0
    while count < 100 and next:
        r = requests.get(raw['next'], headers=headers)
        raw = json.loads(r.text)
        next = raw['next']
        print(next)

        albums.extend(raw['items'])
        count = len(albums)

    print(len(albums))




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
    print(columns)
    print()
    placeholders = ', '.join(['%s'] * len(data))
    print(placeholders)
    print()
    key_placeholders = ', '.join(['{0}=%s'.format(k) for k in data.keys()])
    print(key_placeholders)
    print()
    sql = "INSERT INTO %s ( %s ) VALUES ( %s ) ON DUPLICATE KEY UPDATE %s" % (table, columns, placeholders, key_placeholders)
    print(sql)
    cursor.execute(sql, list(data.values())*2)  
    sys.exit(0)


if __name__ == '__main__':
    main()