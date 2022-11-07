import requests
from bs4 import BeautifulSoup


def main():
    url = "https://www.drugs.com/mtm/anastrozole.html"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    content = soup.find(id="content")
    info = content.find("div", class_="contentBox")
    title = info.find("div", class_="ddc-pronounce-title")
    print(title.text)
    subtitle = info.find("p", class_="drug-subtitle")
    print(subtitle.text)
    related_treatments = info.find("ul", class_="more-resources-list more-resources-list-conditions")
    print(related_treatments.text)



if __name__ == "__main__":
    main()
