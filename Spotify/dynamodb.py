import os
import sys
import boto3
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
        dynamodb = boto3.resource('dynamodb', 
                                region_name='ap-northeast-2', 
                                endpoint_url='http://dynamodb.ap-northeast-2.amazonaws.com')
    except:
        logging.error('could not connect to dynamodb')
        sys.exit(1)
    
    print('Success')

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

    print('Connect')

    headers = get_headers(client_id, client_secret)

    # dynamodb 테이블 불러오기
    table = dynamodb.Table('top_tracks')

    # artist_id 가져오기
    cursor.execute('SELECT id FROM artists')

    # 각 artist_id별 Top-Tracks 정보 접근
    for (artist_id, ) in cursor.fetchall():
        URL = 'https://api.spotify.com/v1/artists/{}/top-tracks'.format(artist_id)
        params = {
            'country': 'US'
        }

        # 정보 호출
        r = requests.get(URL, params=params, headers=headers)
        # raw에 json 형태로 저장
        raw = json.loads(r.text)
        # tracks에 있는 정보들 추출
        for track in raw['tracks']:
            data ={
                'artist_id': artist_id,
            }
            print(artist_id)
            data.update(track)

            # dynamodb table에 put_item 함수를 사용해서 데이터 삽입
            table.put_item(
                Item=data
            )

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

if __name__ == '__main__':
    main()

