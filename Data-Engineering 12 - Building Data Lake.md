# Data-Engineering 12 - Building Data Lake

## AWS S3
> Symple Storage System의 약자, 우리가 만들 Data Lake의 주역?이 됨

### Buckets 생성
- S3 의 폴더 같은 존재
- 우리가 가지고 있는 다양한 데이터를 구분하고 관리하기 위해

    ![ss](DE_img2/screenshot05.png)
    ![ss](DE_img2/screenshot06.png)
    ![ss](DE_img2/screenshot07.png)
    - artist-spotify 라는 이름의 버킷 생성
    - 해당 버킷 안에 여러 파티션들을 생성할것임
    - 파티션을 통해 Spark와 Arthena 등과 연동할 것임

---

### AWS Glue
- AWS 서비스의 분석파트를 보면 있음
- 데이터 레이크로 넘어오면서, 데이터를 저장하는 형식 등이 따로 없었다가,
- 어느 시점부터 키값이 여러개 생긴다는 등의 변화가 생길때,
- AWS Glue를 통해 테이블의 스키마 등도 관리하고, 다른 서비스들과의 연동도 시킴

    ![ss](DE_img2/screenshot08.png)
    ![ss](DE_img2/screenshot09.png)
    - Crawler: 어떤 테이블에 변화가 생기면 알아서 Detect하고 새로운 데이터/ 테이블을 가져올때 바로 반영시켜줌

---

## S3 in Python
> 파이썬으로 S3를 다뤄보겠음

### 연동

    ```python
        # RDS(MySQL) - 아티스트 ID 를 가져오고
        cursor.execute('SELECT id FROM artists')

        # unixtime , 파티션 파악을 위해 시간값을 넣어줘야함
        dt = datetime.utcnow().strftime('%Y-%m-%d')

        # Spotify API를 통해서 데이터를 불러오고


        # .json 타입으로 저장, list of dictionary
        # top_tracks.json이라는 파일이 생기고 거기서 부터 딕셔너리가 한줄한줄 쭉 들어감
        with open('top_tracks.json', 'w') as f:
            for i in top_tracks:
                json.dump(i ,f)
                f.write(os.linesep)

        # 위에서 만든 json 전체를 S3로 inport
        s3 = boto3.resource('s3')

        # 버켓 불러오기
        # readable한 dt(datetime) 파티션을 만들어놔야함(특히 지속적으로 업데이트 되는 데이터들)
        object = s3.Object('artist-spotift', 'dt={}/top-tracks.json',format(dt))

    ```
---

###  
