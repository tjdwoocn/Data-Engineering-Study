import sys
import requests
import base64  # 나의 client id 와 secret key 를 base64 형태로 인코딩해주는 패키지
import json
import logging

client_id = "ab567c2671e34f2ebf5e6acbcb6db44f"
client_secret = "ef7ee3b5900c40048bc142e88f112562"

def main():

    headers = get_headers(client_id, client_secret)

    # Spotify Search API
    params = {
        "q": "BTS",
        "type": "artist",
        "limit": "5", 
    }

    r = requests.get("https://api.spotify.com/v1/search", params = params, headers=headers)

    # try:
    #     r = requests.get("https://api.spotify.com/v1/search", params = params, headers=headers)
    # except:
    #     logging.error(r.text)
    #     sys.exit(1)
    
    if r.status_code != 200:
        logging.error(r.text)

        if r.status_code == 429:

            retry_after = json.loads(r.headers)['Retry-After']
            time.sleep(int(retry_after))

            r = requests.get("https://api.spotify.com/v1/search", params = params, headers=headers)
            
        elif r.status_code == 401:

            headers = get_headers(client_id, client_secret)
            r = requests.get("https://api.spotify.com/v1/search", params = params, headers=headers)

        else:
            sys.exit(1)

    # Get BTS' Albums, BTS ID 값 넣어줘서 찾기
    r = requests.get("https://api.spotify.com/v1/artists/3Nrfpe0tUJi4K4DXYWgMUX", headers=headers)
    
    raw = json.loads(r.text)

    total = raw['total']
    offset = raw['offset']
    limit = raw['limit']
    next = raw['next']

    albums = []
    print(len(raw['items']))
    



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