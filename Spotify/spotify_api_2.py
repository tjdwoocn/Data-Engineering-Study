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

    # 아티스트 리스트 불러오기
    artists = []
    with open('../artist_list.csv', encoding='utf8') as f:
        raw = csv.reader(f)
        for row in raw:
            artists.append(row[0])
    print(len(artists))

    # Spotify Search API
    for a in artists:
        params = {
            "q": a,
            "type": "artist",
            "limit": "1", 
        }
    
        r = requests.get("https://api.spotify.com/v1/search", params = params, headers=headers)
        raw = json.loads(r.text)

        artist = {}

        # 아티스트에 대한 정보가 없는 경우 대비
        try: 
            artist_raw = raw['artists']['items'][0]
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

        except:
            logging.error('NO ITEMS FROM SEARCH API')
            print(artist_raw['name'])
            continue
    
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