# 개인 정보를 위해 일부 과정 생략 

import os
from pathlib import Path
import webbrowser

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

_CURRENT = Path(os.path.abspath(__file__)).parent.absolute()
_PARENT = Path(_CURRENT).parent.absolute()
_HTML = os.path.join(_PARENT, "src", "index.html")
_DATA = os.path.join(_PARENT, "성적.csv")


class Simulator(object):
    def __init__(self):
        df = pd.read_csv(_DATA)
        self._df = self._preprocess(df)

    def _preprocess(self, df):
        cols = df.columns.values.tolist()
        df.columns = list(map(lambda x: str(x).replace(" ", ""), cols))
        df["등급"] = df["등급"].map(lambda x: str(x).strip().upper())
        df["시수"] = df["시수"].map(lambda x: str(x).strip()).astype(int)
        df["분류"] = df["분류"].map(lambda x: str(x).strip().lower()).astype(str)
        df["분류2"] = df["분류2"].map(lambda x: str(x).strip().lower()).astype(str)
        return df

    def _get_continuous_grades(self, subject):
        cond = (self._df["분류"] == subject) & (self._df["분류2"] != "ca")
        return self._df.loc[cond, ["등급", "시수"]].to_numpy().astype(np.int32)

    def _get_grades_by_label(self, subject, label):
        """Label: 'ca', 'se', 'co"""
        cond = (self._df["분류"] == subject) & (self._df["분류2"] == label)
        grades = self._df.loc[cond, ["등급", "시수"]].to_numpy()
        if label != "ca":
            grades = grades.astype(np.int32)
        return grades

    def _get_mean_continuous_grade(self, arr):
        arr = np.array(arr, dtype=np.int32)
        scores = [grade * hour for grade, hour in arr]
        hours = arr[:, 1]
        return np.sum(scores) / np.sum(hours)

    def _get_weighted_discrete_grade(self, arr, weights: dict):
        grades = arr[:, 0].copy()
        for disc, cont in weights.items():
            grades = np.where(grades == disc, cont, grades)
        arr[:, 0] = grades
        return arr

    def _sort_grade_array(self, arr, reverse=False, max=None):
        if reverse:
            arr = sorted(arr, key=lambda row: (row[0], int(row[1])), reverse=True)
        else:
            arr = sorted(arr, key=lambda row: (row[0], -int(row[1])))
        if max:
            arr = arr[:max]
        return np.array(arr)

    def uni_name(self):
        """대학별 점수 환산법"""
        pass

    def get_grades(self):
        return [
            self.uni_name(),
            # 이하 생략
        ]


class HTMLContent(object):
    def __init__(self, grades):
        self._html = _HTML
        self._update_score(grades)

    def _format_grade(self, grades):
        formatted = list()
        numbers = (float, int)
        for partial_grade, all_grade in grades:
            assert isinstance(all_grade, numbers) and isinstance(
                partial_grade, numbers
            ), "계산 오류"
            formatted.append(f"{partial_grade:.2f} ({all_grade:.2f})")
        return formatted

    def _update_score(self, grades):
        with open(self._html, encoding="UTF-8") as html_file:
            soup = BeautifulSoup(html_file.read(), features="html.parser")

            tags = soup.find_all("td", "myGrade")
            grades = self._format_grade(grades)

            for tag, grade in zip(tags, grades):
                tag.string.replace_with(grade)

            html = str(soup)

        # Write new contents to test.html
        with open(self._html, "w", encoding="UTF-8") as new_html_file:
            new_html_file.write(html)

    def open(self):
        webbrowser.open(url=self._html, new=2, autoraise=True)
