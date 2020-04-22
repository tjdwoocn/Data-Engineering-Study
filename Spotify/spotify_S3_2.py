import sys
import os
import logging
import boto3
import requests
import base64
import pymysql
import json
from datetime import datetime
import pandas as pd
import jsonpath

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
    cursor.execute('SELECT id FROM artists LIMIT 10')

    # jsonpath 패키지를 통해, 해당 path안에서 데이터를 가져올때,
    # 지정된 키를 참고하여 좀 더 빠르고 쉽게 가져옴
    top_track_keys = {
        'id': 'id',
        'name': 'name',
        'popularity': 'popularity',
        'external_url': 'external_urls.spotify' 
    }

    # Top Tracks - Spotify 가져오고
    top_tracks = []
    for (id, ) in cursor.fetchall():

        URL = 'https://api.spotify.com/v1/artists/{}/top-tracks'.format(id)
        params = {
            'country' : 'US'
        }
        r = requests.get(URL, params=params, headers=headers)
        raw = json.loads(r.text)

        for i in raw['tracks']:
            top_track = {}
            for k,v in top_track_keys.items():
                # k, key로 jsonpath 사용하여 v,value에 바로 접근/찾음
                top_track.update({k: jsonpath.jsonpath(i, v)})
                top_track.update({'artist_id': id})
                top_tracks.append(top_track)
        
    # List of dictionaries, Parquet화
    top_tracks = pd.DataFrame(top_tracks)
    top_tracks.to_parquet('top_tracks.parquet', engine='pyarrow', compression='snappy')

   # unixtime 
    dt = datetime.utcnow().strftime('%Y-%m-%d')

    # S3에 import
    s3 = boto3.resource('s3')

    # 버켓 불러오기 (기존의 json이 아닌 parquet으로)
    object = s3.Object('artist-spotift', 'dt={}/top-tracks.parquet',format(dt))
    data = open('top-tracks.parquet', 'rb')
    object.put(Body=data)

    # audio features
    audio_features = 

    # track_ids, top_tracks안의 id값만 가져오기
    track_ids = [i['id'][0] for i in top_tracks]
    tracks_batch = [track_ids[i: i+100] for i in range(0, len(track_ids), 100)]

    for i in tracks_batch:
        ids = ','.join(i)
        URL = 'https://api.spotify.com/v1/audio-features/?ids={}'.format(ids)

        r = requests.get(URL, headers=headers)
        raw = json.loads(r.text)

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


if __name__ == "__main__":
    main()
