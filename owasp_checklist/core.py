import re
from typing import Any, Dict, List

import requests
from bs4 import BeautifulSoup


def get(language: str, version: str) -> List[Dict[Any, Any]]:
    urls = list_urls(language, version)
    res = []
    for url in urls:
        res += parse(url)
    return res


def list_urls(language: str, version: str) -> List[str]:
    if language == "en":
        url = f"https://github.com/OWASP/ASVS/tree/master/{version}/en"
    elif language == "ja":
        url = f"https://github.com/owasp-ja/asvs-ja/tree/master/{version}/ja"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    urls = []
    for link in soup.find_all("a", attrs={"href": re.compile(".*0x[0-9]+-V[0-9]+")}):
        urls.append("https://raw.githubusercontent.com" + re.sub("/blob", "", link.get("href")))
    return urls


def parse(url: str) -> List[Dict[Any, Any]]:
    response = requests.get(url)
    category_number = ""
    category = ""
    items = []
    for line in response.text.split("\n"):
        m = re.match("##", line)
        if m:
            category_number = ""
            category = ""
            m = re.match("## (V.+?) (.+)", line)
            if m:
                category_number = m.group(1).strip()
                category = m.group(2)
        if category != "":
            m = re.match(r"\|.+", line)
            if m:
                columns = [column.strip() for column in line.split("|")]
                columns = columns[1:]
                if columns[0] == "#" or columns[0] == ":---:":
                    continue
                number = columns[0]
                description = columns[1]
                level_1 = columns[2]
                level_2 = columns[3]
                level_3 = columns[4]
                cwe = columns[5]
                items.append(
                    {
                        "category_number": category_number,
                        "number": re.sub(r"\*", "", number),
                        "category": category,
                        "description": description,
                        "level_1": level_1,
                        "level_2": level_2,
                        "level_3": level_3,
                        "cwe": cwe,
                    }
                )
    return items


def out(items: List[Dict[Any, Any]], format: str, level: int) -> None:
    items = [item for item in items if item[f"level_{level}"]]
    if format == "markdown":
        previous_item = {"category_number": ""}
        for item in items:
            if previous_item["category_number"] != item["category_number"]:
                previous_item = item
                print("")
                print(f"## {item['category_number']} {item['category']}")
                print("")
                print("| # | Description | L1 | L2 | L3 | CWE |")
                print("| :---: | :--- | :---: | :---:| :---: | :---: |")

            no = f"**{item['number']}**"
            print(
                f"| {no} | {item['description']} | {item['level_1']} | {item['level_2']} | {item['level_3']} | {item['cwe']} |"
            )
