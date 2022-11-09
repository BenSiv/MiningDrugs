import requests
from bs4 import BeautifulSoup


def scrape_page(url):
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
    related_drugs = info.find("div", class_="ddc-inset-text")
    print(related_drugs.text)
    """side_effects = info.find("div", class_="contentBox")
    print(side_effects.text)
    more_resources = info.find("div", class_="more-resources")
    print(more_resources.text)"""
    # the last two are in info.text but can't find them
    return 'success'


def main():
    info_text = scrape_page("https://www.drugs.com/mtm/anastrozole.html")
    print(info_text)


if __name__ == "__main__":
    main()
