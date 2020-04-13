# Data-Engineering 07 - Data, RDBMS

## Data Types
> Schema에서 저장되는/쓰이는 각 데이터별로 타입의 종류가 다르고, 타입별로 사용방법 또한 다르다

### SQL Data Types

![ss](DE_img/screenshot97.png)


- Numeric Data

    ![ss](DE_img/screenshot98.png)

- Date and Time Data

    ![ss](DE_img/screenshot99.png)
    - unix time -> 한국은 KST

- Character and String Data

    ![ss](DE_img/screenshot100.png)
    - string의 경우 간단하게 최대 용량만큼 받아들일 수 있게 셋팅 할수도 있지만,
    - resource를 효율적으로 쓰기 위해서는 딱 필요한 범위 만큼으로만 지정 해두는것이 좋음
    - 한국인의 이름 Char 경우 10글자 이상 나오는 경우는 정말 드뭄

---

## Relational Database
> 관계형 데이터베이스, 현재 가장 많이 쓰이고 있는 데이터 베이스 형식 중 하나

### Database
- 데이터를 가지고 있는, 정리되어 있는 데이터들의 컬렉션
![ss](DE_img/screenshot101.png)

### 관계형 데이터 모델의 데이터베이스, RDB
- 데이터를 표현하는 모델, 2차원의 테이블 형태로
![ss](DE_img/screenshot102.png)

### 속성 및 특징
![ss](DE_img/screenshot103.png)
![ss](DE_img/screenshot104.png)
- 각 테이블 안의 데이터들이 서로 관계/연결고리를 가지고 있음

### RDB
- Normalization(Reduce Redundancy): 복수의 데이터가 들어가는 것을 최대한 방지, 데이터 테크닉
    ![ss](DE_img/screenshot105.png)
    
- 정규화 전/후
  
    ![ss](DE_img/screenshot106.png)
    ![ss](DE_img/screenshot107.png)

### 종류
- 전체적으로 비슷한 특성을 가지고 있지만
- 각 데이터베이스 별로 서로의 장/단점이 다름
  
    ![ss](DE_img/screenshot108.png)


---

