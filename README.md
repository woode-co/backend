# Woodeco RecSys (refactored)

## 0. Requirements
**IMPORTANT : `python >= 3.10` and  `.env` file**

`3.9` 아래 버전은 호환성 테스트를 못해봤음. 개발 환경은 `3.10.14` 

```bash
> pip install pandas openai dotenv haversine
# 라이브러리들끼리 dependency issue 없어서 버전 고려안하고 설치 가능
```

## 1. `main()` 실행

`./main.py`에 선언된 `main()`를 실행하면,
`epoch`와 동일한 개수의 추천 코스를 포함한 LLM의 response가 나오게된다.
해당 값은 `./cache/{실행시각}.cache` 로 저장된다.

다음과 같이 테스트해볼 수 있다.
```bash
> python main.py
```  

## 2. `check()` 실행
`check()` 함수의 반환 값 = **'json 형식의 데이트 코스 추천 결과의 리스트'**
그러므로, `main()` 실행의 결과를 확인하려면 반드시 `check()`를 실행해야한다.  
* `check(save=True)` 로 실행하면 json 파일을 저장해준다는 점 유의

다음과 같이 테스트해볼 수 있다.
```bash
> python check.py
```  