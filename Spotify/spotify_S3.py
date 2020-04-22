import sys
import os
import logging
import boto3
import requests
import base64
import pymysql
import json
from datetime import datetime

client_id = "ab567c2671e34f2ebf5e6acbcb6db44f"
client_secret = "ef7ee3b5900c40048bc142e88f112562"

host = 'data-engineering.c9ck0xgcwbcx.us-east-2.rds.amazonaws.com'
port = 3306
username = 'SJ'
database = 'production'
password = ''


def main():

    try:
        # MySQL 커넥트
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

    # RDS(MySQL) - 아티스트 ID 를 가져오고
    cursor.execute('SELECT id FROM artists')

    # unixtime 
    dt = datetime.utcnow().strftime('%Y-%m-%d')

    for (id, ) in cursor.fetchall():

        # Spotify API를 통해서 데이터를 불러오고

    # .json 타입으로 저장
    with open('top_tracks.json', 'w') as f:
        for i in top_tracks:
            json.dump(i ,f)
            f.write(os.linesep)

    # S3에 import
    s3 = boto3.resource('s3')
    # 버켓 불러오기
    object = s3.Object('artist-spotift', 'dt={}/top-tracks.json',format(dt))
    data = open('top-tracks.json', 'rb')
    object.put(Body=data)


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


def if __name__ == "__main__":
    main()
