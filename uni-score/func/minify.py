import os
import re
from pathlib import Path

from bs4 import BeautifulSoup
import htmlmin

_CURRENT = Path(os.path.abspath(__file__)).parent.absolute()
_PARENT = Path(_CURRENT).parent.absolute()
_HTML = os.path.join(_PARENT, "src", "index.html")
_CSS = os.path.join(_PARENT, "src", "main.css")

# HTML
with open(_HTML, encoding="UTF-8") as html_file:
    soup = BeautifulSoup(html_file.read(), features="html.parser")

minified_html = htmlmin.minify(str(soup))

with open(_HTML, "w", encoding="UTF-8") as new_html_file:
    new_html_file.write(minified_html)

# CSS
with open(_CSS, encoding="UTF-8") as css_file:
    css = css_file.read()

minified_css = re.sub(r"[\n\t]", "", css)
minified_css = re.sub(r" +", " ", minified_css)
with open(_CSS, "w", encoding="UTF-8") as new_css_file:
    new_css_file.write(minified_css)