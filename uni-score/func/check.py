"""Client Local PC에서 실행 시 활용"""

import os
import sys
from pathlib import Path
import importlib.util

import pandas as pd 

_CURRENT = Path(os.path.abspath(__file__)).parent
_PARENT = Path(_CURRENT).parent.absolute()
_DATA = os.path.join(_PARENT, "src", "성적.csv")
_HTML = os.path.join(_PARENT, "src", "index.html")
_CSS = os.path.join(_PARENT, "src", "main.css")
_JS = os.path.join(_PARENT, "src", "main.js")

templates = [(_HTML, "index.html"), (_CSS, "main.css"), (_JS, "main.jss")]
package_names = ["numpy", "bs4", "pandas", "openpyxl"]
columns = ["등급", "시수", "분류", "분류2"]
one2nine = map(lambda x: str(x), range(1, 10))
grades_values = ["A", "B", "C", "P", "F"] + list(one2nine)
label1_values = ["ko", "ma", "en", "so", "sc", "ex"]
label2_values = ["ca", "se", "co", "pf"]

if __name__ == "__main__":
    ##############################################################################
    print("Python 버전 확인: ", end="")
    py_version = sys.version.split(" ")[0]
    print(py_version)
    version_info = py_version.split('.')
    if (version_info[0] != "3") or (int(version_info[1]) < 6):
        print("[WARNING] 3.6 버전 이상이 필요합니다.")
        exit()
    ##############################################################################
    print("패키지 설치 확인: ", end="")
    is_error = False
    for package in package_names:
        spec = importlib.util.find_spec(package)
        if spec is None:
            print(f"\n [WARNING] {package}가 설치되지 않았습니다.")
    if is_error:
        print(" [INFO] '설치.bat'을 실행해 필요한 패키지를 설치할 수 있습니다.")
    else:
        print("정상")
    ##############################################################################
    print("템플릿 탐색: ", end="")
    is_error = False
    for path, name in templates:
        if not os.path.exists(path):
            print(f"\n [WARNING] src 폴더 내에 '{name}'라는 이름의 파일을 찾지 못했습니다.")
            is_error = True
    if not is_error:
        print("성공")

    ##############################################################################
    print("데이터 불러오기: ", end="")
    if os.path.exists(_DATA):
        try:
            df = pd.read_excel(
                _DATA, sheet_name="grade", header=0, usecols=[2, 3, 4, 5]
            )
            print("성공")
        except Exception as exp:
            print(f"오류 발생 ({exp})")
            exit()
    else:
        print(f"\n [WARNING] 폴더 내에 '성적.xlsx'라는 이름의 파일을 찾지 못했습니다.")
        exit()

    ##############################################################################
    print("항목명 확인: ", end="")
    cols = df.columns.values.tolist()
    cols = list(map(lambda x: str(x).replace(" ", ""), cols))
    if cols == columns:
        print("정상")
    else:
        print(f"\n [WARNING] 항목명은 학기, 과목 + {columns}로 구성되어야 합니다.")

    ##############################################################################
    print("등급 값 확인: ", end="")
    grades = df["등급"].map(lambda x: str(x).strip().upper()).astype(str).unique().tolist()
    temp = grades.copy()
    for grade in grades:
        if grade in grades_values:
            temp.remove(grade)

    if len(temp) == 0:
        print("정상")
    else:
        print(f"\n [WARNING] 등급 값은 {grades_values}로만 구성되어야 합니다.", end=" ")
        print(f"{temp}은 정상 값이 아닙니다.")

    ##############################################################################
    print("시수 값 확인: ", end="")
    times = df["시수"].map(lambda x: str(x).strip())
    is_error = False
    for time in times:
        if not str(time).isdigit():
            print("\n [WARNING] 시수 값은 정수로만 구성되어야 합니다.")
            print(f"{time}은 정상 값이 아닙니다.")
            is_error = True
        if not (0 < int(time) < 6):
            print("\n [WARNING] 시수 값은 1 ~ 5 사이의 값으로 구성되어야 합니다.")
            print(f"{time}은 정상 값이 아닙니다.")
            is_error = True
        if is_error:
            break
    if not is_error:
        print("정상")

    ##############################################################################
    print("분류 값 확인: ", end="")
    label1 = df["분류"].map(lambda x: str(x).strip().lower()).astype(str).unique().tolist()
    label2 = df["분류2"].map(lambda x: str(x).strip().lower()).astype(str).unique().tolist()
    temp1 = label1.copy()
    temp2 = label2.copy()
    for label in label1:
        if label in label1_values:
            temp1.remove(label)
    for label in label2:
        if label in label2_values:
            temp2.remove(label)    

    if len(temp1) + len(temp2) == 0:
        print("정상")
    elif len(temp1) != 0:
        print(f"\n [WARNING] 분류는 {label1_values}로 구성되어야 합니다.", end=" ")
        print(f"{temp1}은 정상적인 값이 아닙니다.")
    elif len(temp2) != 0:
        print(f"\n [WARNING] 분류는 {label2_values}로 구성되어야 합니다.", end=" ")
        print(f"{temp2}은 정상적인 값이 아닙니다.")

    ##############################################################################
    print("[INFO] 검사가 종료되었습니다.")