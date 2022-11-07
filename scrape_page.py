import requests
from bs4 import BeautifulSoup


def main():
    url = "https://www.drugs.com/mtm/ampicillin.html"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    content = soup.find(id="content")
    title_head = content.find("div", class_="contentHead")
    title = title_head.find("li", class_="ddc-breadcrumb-item active")
    print(title.text)


if __name__ == "__main__":
    main()
