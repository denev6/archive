# 대학별 점수 환산 프로그램

- 목적: 특정 개인의 대학 환산 점수 계산 및 비교
- 수행 기간: Dec 20, 2022 ~ Jan 1, 2023

*개인 정보를 위해 일부 코드 및 데이터는 삭제되었습니다. 

## Requirements
- Python >= 3.6
- numpy
- pandas
- bs4
- htmlmin

## How to

- `HTML`, `CSS`, `Js`로 템플릿 제작 
- `numpy`, `pandas`로 성적 계산
- `bs4`로 `HTML` 내 정보 업데이트 
- `Netlify` - `Github-repo` 연동 
- `/src`를 `Netlify`로 호스팅
- URL 정보 공유 ( i.e. "uni.netlify.app" )

```bash
$ python ./func/main.py
$ python ./func/minify.py

$ git ...
$ git push
```
