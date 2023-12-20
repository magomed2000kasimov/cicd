import requests
from bs4 import BeautifulSoup

msu_news_url = "https://math.msu.ru/news"
page_count = 20
last_news = {}

for page in range(page_count):
    msu_page_url = msu_news_url + f"?page={page}"
    response = requests.get(url=msu_page_url)
    parser = BeautifulSoup(response.text)
    page_news = parser.findAll('div', class_='view-content')[0]
    page_news = page_news.findChildren('div', recursive=False)
    for cur_news in page_news:
        title = cur_news.h3.a.text
        all_p = cur_news.findChildren('p')
        del all_p[-1]
        text_of_news = ""
        for p in all_p:
            text_of_news += p.text

        category = cur_news.findAll("div", class_="field-item even")[-1].a.text
        date_of_news = cur_news.findAll('span')[-1].find("li").text

        #добавление в словарь новостей
        news_dict = {"text": text_of_news, "date": date_of_news}
        if not text_of_news:
            continue
        if category not in last_news:
            last_news[category] = []
        last_news[category].append(news_dict)

with open("news.txt", "w") as file:
    for category in last_news:
        #file.write('\t' + category + '\n\n')
        print('\t' + category + '\n\n')
        for news in last_news[category][:3]:
            #file.write(news["text"] + "\n")
            print(news["text"] + "\n")
            #file.write(news["date"] + "\n\n")
            print(news["date"] + "\n")
        #file.write("\n\n")
        print("\n")


