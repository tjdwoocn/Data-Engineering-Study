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

## 