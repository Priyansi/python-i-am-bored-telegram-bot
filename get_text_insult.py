import requests
import random
from bs4 import BeautifulSoup


def get_insult():
    toss = random.randint(0, 2)  # gets a number either 0 or 1
    if toss:
        response = requests.get("https://insult.mattbas.org/api/insult")
        content = response.content.decode("utf8")
    else:
        response = requests.get(
            "http://robietherobot.com/Shakespearean-Insult-Generator.htm")
        content = response.content.decode("utf8")
        soup = BeautifulSoup(content, "lxml")
        content = "Thou art a "+str(soup.find_all("h1")[1]).replace(
            "<h1>", " ").replace("</h1>", " ").strip().lower().replace("  ", " ")  # hacky but consistent
    return content


if __name__ == "__main__":
    print(get_insult())
