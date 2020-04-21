import os
import sys
import boto3
import requests
import base64  # 나의 client id 와 secret key 를 base64 형태로 인코딩해주는 패키지
import json
import logging
import pymysql
import csv
from boto3.dynamodb.conditions import Key, Attr # Querying와 Scanning을 쓰기 위해 필요


def main():

    try:
        dynamodb = boto3.resource('dynamodb', 
                                region_name='ap-northeast-2', 
                                endpoint_url='http://dynamodb.ap-northeast-2.amazonaws.com')
    except:
        logging.error('could not connect to dynamodb')
        sys.exit(1)

    print('Success')

    table = dynamodb.Table('top_tracks')
    # # key 값으로는 우리가 설정한 모든 key값이 있어야만 사용가능
    # response = table.get_item(
    #     Key={
    #         'artist_id': '7hJcb9fa4alzcOq3EaNPoG',
    #         'id': '6YbhspuOar1D9WSSnfe7ds'
    #     }
    # )
    # item = response['item']
    # print(item)

    # Querying
    response = table.query(
        KeyConditionExpression = Key('artist_id').eq('0L8ExT028jH3ddEcZwqJJ5'),
        FilterExpression = Attr('popularity').gt(80)
    )
    print(response['Items'])
   

if __name__ == '__main__':
    main()

