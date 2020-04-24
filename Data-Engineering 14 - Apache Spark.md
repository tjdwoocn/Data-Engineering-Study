# Data-Engineering 14 - Apache Spark

## Apache Spark란?
> 빅데이터를 처리하는 하나의 시스템, 하둡의 속도적인 부분을 개선한 진화버전(?)

### Spark Overview
- 방대한 데이터를 효율적으로(시간, 비용) 처리하기 위해 쓰임

    ![ss](DE_img2/screenshot29.png)

- 우리는 스파크 기반의 웹 UI인 Zeppline을 쓸것임
    - 스파크로 처리하는 것을 시각적으로 확인가능

### Map Reduce
- 데이터가 방대한 양으로 늘어날때, 해당 데이터를 처리하는 방식에서 고려해야할 부분이 많음
- 좀더 효율적으로 처리하기 위해 데이터를 맵핑, 병렬적으로 처리, reducing 하는 방법
  
    ![ss](DE_img2/screenshot30.png)
    - 데이터가 여러개로 쪼개져 있음(partition)
    - node: 병렬적 데이터 처리를 위한 processing term, 저장공간


- ex)
  
    ![ss](DE_img2/screenshot31.png)
    - input -> map -> shuffle -> reduce -> output
    - 구글의 page rank, word count
