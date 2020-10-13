import pandas as pd
import requests
from bs4 import BeautifulSoup


def scrape_skills():
    response = requests.get(
        "https://fireemblem.fandom.com/wiki/List_of_Skills_in_Fire_Emblem_Awakening"
    )

    soup = BeautifulSoup(response.content, "html.parser")

    tbl = soup.find("table", {"class", "article-table"})

    col_names = [header.text.strip() for header in tbl.findAll("th")]

    data = []
    for row in tbl.findAll("tr"):
        data.append([d.text.strip().replace("-", "") for d in row.findAll("td")])

    df = pd.DataFrame(data, columns=col_names)
    df.drop("Icon", axis=1, inplace=True)
    df.drop(0, axis=0, inplace=True)
    return df
