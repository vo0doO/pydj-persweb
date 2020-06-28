from project.apps.curiosity.parser.curiosity_one_post import *
from project.apps.curiosity.models import PostAuthor, Post, PostComment
import requests
import datetime
from django.shortcuts import get_or_create


FIRST_POST_INDEX = 1
TIMEOUT = 100


class PageParser:
    """Парсер списка постов"""

    url = None
    html = None
    soup = None
    cards = None

    def __init__(self, *args, **kwargs):
        if kwargs is not None: self.url = kwargs["url"]
        with open(file='d:\projects\py\curiosity-to-vk\\topics\discovery.html', encoding="utf-8",
                  mode="r") as f: self.html = f.read()
        self.soup = BeautifulSoup(self.html, "lxml")
        self.cards = self.soup.find_all("div", {"class": "articles__item"})


class CardIter:
    """Карточка поста"""

    link = None
    image = None
    title = None

    def __init__(self, data):
        self.data = data
        self.index = len(data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]


class CardParser:

    FOR_REPLACE_WORDS = "Discovery Channel"
    TO_REPLACE_WORDS = "Любопытство"
    link_sufix = "http://www.discoverychannel.ru/articles/"

    def __init__(self, card):
        self.card_link = card.find("a", {"class": "show-card__link"})["href"],
        self.card_image = card.find("img", {"class": "show-card__pic"})["src"],
        self.card_title = card.find("div", {"class": ["show-card__name title title_h4"]}).text
        self.article_slug = self.card_link[0].split('/')[2]
        self.article_page = requests.get(self.link_sufix + self.article_slug + "/")
        self.article_soup = BeautifulSoup(self.article_page.text, "lxml")
        self.topic_container = self.article_soup.find("div", {"class": "topic__container container"})
        self.text = [top.text for top in self.topic_container.find_all("p")]
        self.stop = "stop"

    def format_text(self):
        data = self.text[0:-1]
        self.text = str()
        for line in data:
            if self.FOR_REPLACE_WORDS in line:
                line.replace(self.FOR_REPLACE_WORDS, self.TO_REPLACE_WORDS)
            self.text = self.text + line
        return self.text

    def img_downloader(self):
        url_sufix = self.card_image[0]
        url_prefix = "http://www.discoverychannel.ru"
        if url_sufix is not None:
            res = requests.get(url_prefix, "b")
            with open(str("pydj-persweb/project/apps/curiosity/static/curiosity/img/" + self.article_slug + ".png"), 'wb') as zero:
                zero.write(res.content)
        else:
            print("Ошибка загрузки изображения")
        print("Скачены изображениея")


def post_maker(request)
    pp = PageParser(url=None)
    ci = CardIter(data=pp.cards)
    count = 0
    for c in ci:
        count = count + 1
        if count <= FIRST_POST_INDEX:
            continue
        result = False
        while result == False:
            try:
                cp = CardParser(card=c)
                cp.format_text()
                print(f"{count}")
                cp.img_downloader()
                draw(channel_ru=cp.card_title, title_ru="Power by@vo0doo", img_path=str("pydj-persweb/project/apps/curiosity/static/curiosity/img/" + self.article_slug + ".png"))
                resul, post = Post.objects.get_or_create(
                    author=request.session.user.id,
                    text=cp.text,
                    title=cp.card_title,
                    title_en = "",
                    text_en = "",
                    html = cp.topic_container,
                    url = ,
                    channel = 1,
                    tags = 1,
                    created_date = datetime.datetime.now(),
                    pub_date = datetime.datetime.now(),
                    rewrite_date = datetime.datetime.now(),
                    slug = cp.article_slug,
                    img = str("pydj-persweb/project/apps/curiosity/static/curiosity/img/" + self.article_slug + ".png"),
                    status = "Опубликован",
                    )
                if post:
                    post.save(
                    )
                else:
                    continue
            except Exception as err:
                logger.error(err)
                result = False
        time.sleep(TIMEOUT)
        continue

if __name__ == "__main__":
    __import__()