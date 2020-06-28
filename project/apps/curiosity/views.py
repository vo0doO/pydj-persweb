import logging
import os
import sys
import time
import urllib
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.core.files import File
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from authentication.models import CustomUser as User
from project.apps.curiosity.models import (Channel, Post,  # PostAuthor
                                           Tag)
from project.apps.curiosity.models import Image as CImage
logger = logging.getLogger(__name__)

def get_logs():
    fmt = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s')

    file_handler = logging.FileHandler(filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), "parser", "curiosity-to-vk.log"))
    file_handler.setFormatter(fmt)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(fmt)

    root_logger = logging.getLogger()

    root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)

    root_logger.setLevel(logging.INFO)
    return root_logger

l = get_logs()
class PostListView(ListView):
    models = Post
    queryset = Post.objects.order_by('-pub_date')
    context_object_name = 'post_list'
    template_name="curiosity/post_list.html"


class PostCreateView(CreateView):
    models = Post
    fields = "__all__"


class PostUpdateView(UpdateView):
    models = Post
    fields = "__all__"


class PostDetailView(DetailView):
    models = Post
    query_pk_and_slug = True
    queryset = Post.objects.all()
    fields = "__all__"

    def get_queryset(self):
        return self.queryset.filter(slug=self.kwargs.get('slug'))


class PostDeleteView(DeleteView):
    model = Post
    fields = "__all__"


class TagListView(ListView):
    models = Post
    fields = "__all__"

    paginate_by=10


class TagCreateView(CreateView):
    models = Post
    fields = "__all__"


class TagUpdateView(UpdateView):
    models = Post
    fields = "__all__"


class TagDetailView(DetailView):
    models = Post
    query_pk_and_slug = True
    queryset = Post.objects.all()
    fields = "__all__"

    def get_queryset(self):
        return self.queryset.filter(slug=self.kwargs.get('slug'))


class TagDeleteView(DeleteView):
    model = Post
    fields = "__all__"


class ChannelListView(ListView):
    models = Post
    fields = "__all__"

    paginate_by=10


class ChannelCreateView(CreateView):
    models = Channel
    fields = "__all__"


class ChannelUpdateView(UpdateView):
    models = Channel
    fields = "__all__"


class ChannelDetailView(DetailView):
    models = Channel
    query_pk_and_slug = True
    queryset = Channel.objects.all()
    fields = "__all__"

    def get_queryset(self):
        return self.queryset.filter(slug=self.kwargs.get('slug'))


class ChannelDeleteView(DeleteView):
    model = Channel
    fields = "__all__"


class UserListView(ListView):
    models = User
    fields = "__all__"

    paginate_by=10


class UserCreateView(CreateView):
    models = User
    fields = "__all__"


class UserUpdateView(UpdateView):
    models = User
    fields = "__all__"


class UserDetailView(DetailView):
    models = User
    query_pk_and_slug = True
    queryset = User.objects.all()
    fields = "__all__"

    def get_queryset(self):
        return self.queryset.filter(slug=self.kwargs.get('slug'))


class UserDeleteView(DeleteView):
    model = User
    fields = "__all__"
"""
    class PostAuthorListView(ListView):
    models = PostAuthor
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super(PostAuthorListView, self).get_context_data(**kwargs)
        context['author'] = get_object_or_404(PostAuthor, pk=self.kwargs['pk'])
        return context
    paginate_by=10


    class PostAuthorCreateView(CreateView):
        models = PostAuthor
        fields = "__all__"


    class PostAuthorUpdateView(UpdateView):
        models = PostAuthor
        fields = "__all__"


    class PostAuthorDetailView(DetailView):
        models = PostAuthor
        queryset = PostAuthor.objects.all()
        fields = "__all__"

        def get_queryset(self):
            return self.queryset.filter(user=self.kwargs.get('user'))


    class PostAuthorDeleteView(DeleteView):
        model = PostAuthor
        fields = "__all__"
"""
class PostByChannelListView(ListView):
    model = Post


class PostByTagListView(ListView):
    model = Post


class PostByAuthorListView(LoginRequiredMixin, ListView):
    models = Post
    query_pk_and_slug = True
    queryset = Post.objects.all()
    template_name = "curiosity/pubpost_list_author_user.html"

    paginate_by=10

    def get_queryset(self):
        return self.queryset.filter(author_id=self.request.user.id)


def read_db(PATH_TO_DB):
    links = []
    with open(PATH_TO_DB, 'r') as f:
        link_list = f.readlines()
        for link in link_list:
            if str('\n') in str(link):
                link = str(link).replace('\n', '')
            links.append(str(link))
    return links

def index(request):
    """Просмотр функции для главной страницы сайта."""

    # Сформировать подсчеты некоторых из основных объектов
    num_posts = Post.objects.all().count()
    num_channels = Channel.objects.all().count()

    # Опубликованные посты (status = 'a')
    num_pub = len([post.status for post in Post.objects.all() if post.status == "Опубликован"])
    num_new = len([post.status for post in Post.objects.all() if post.status == "Обнаружен"])
    # «Все ()» подразумевается по умолчанию.    
    num_tags = Tag.objects.count()

    # Количество посещений этой cnhfybws, поскольку, подсчитанных в переменной сеанса.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    context = {
        'num_new': num_new,
        'num_posts': num_posts,
        'num_channels': num_channels,
        'num_pub': num_pub,
        'num_tags': num_tags,
        'num_visits': num_visits,
    }

    # Рендер шаблон HTML index.html с данными в переменном контексте
    return render(request, 'curiosity/index.html', context=context)

def magic_publishe(self, request):

    self.publish_post(request)
    return HttpResponseRedirect('/curiosity/')

def get_new_posts_of_file(request):

    Post.get_new_posts_of_file()
    return HttpResponseRedirect('/curiosity/')

def get_new_posts_of_network(request):
    Post.get_new_posts_of_network()
    return HttpResponseRedirect('/curiosity/')

def check_channel(channel):
    if channel is None:
        return
    elif Channel.objects.get_or_create(name=channel)[1]:
        channel = Channel.objects.get_or_create(name=channel)[0]
        channel.save()
        return channel
    else:
        channel = Channel.objects.get_or_create(name=channel)[0]
        return channel

def check_tags(tags):
    tags_obj = []
    if tags is None:
        return
    else:
        for tag in tags:
            if Tag.objects.get_or_create(name=tag)[1]:
                tag_obj = Tag.objects.get_or_create(name=tag)[0]
                tag_obj.save()
                tags_obj.append(tag_obj)
            else:
                tag_obj = Tag.objects.get_or_create(name=tag)[0]
                tags_obj.append(tag_obj)
    return tags_obj

def add_tags(post, tags):
    for tag in check_tags(tags):
        post.tags.add(tag)        

def add_image(post, img_href, channel, title):
    img_url = "https://dw8stlw9qt0iz.cloudfront.net/" + img_href[5] + ".png"
    name = urlparse(img_url).path.split('/')[-1]

    content = urllib.request.urlretrieve(img_url)

    draw_img_temp_path = draw(channel, title, img_path=content[0])

    file = File(open(draw_img_temp_path, "rb"))

    post.fimg.save(name, file, save=True)
 
    post.img

    post.save()

    file.close()

def create_image(href, post):
    img_url = "http://www.discoverychannel.ru" + href[0] + ".png"
    name = urlparse(img_url).path.split('/')[-1].replace(".png", "")

    image = CImage.objects.get_or_create(
        id=name,
        urls_x300=", ".join([hr for hr in href if str("x300") in hr]),
        urls_x600=", ".join([hr for hr in href if str("x600") in hr])
        )[0]

    image.save()

    image.post = post

    image.save()

def checkposts(myposts, hrefs):
    from urllib.parse import urlparse
    hrefs_to_posts = []
    my_slugs = [post.slug for post in myposts]
    if len(myposts) == 0:
        return hrefs
    else:
        for href in hrefs:
            slug = urlparse(href).query.replace('q=cache:3XI5iWomPXMJ:http://curiosity.com/topics/', '')
            if slug not in my_slugs:
                hrefs_to_posts.append(href)
            else:
                logger.info(f"The post published: {slug}")
        return hrefs_to_posts

def parser(href):
    r = requests.get(href)
    html = r.text.encode("utf-8")
    soup = BeautifulSoup(html, "lxml")
    html = soup._most_recent_element
    soup = BeautifulSoup(html, "lxml")
    page = soup.find("div", {"class": "topic-page"})
    content_header = page.find_all("div", {"class": "image-header"})
    contents = page.find("div", {"class": ["topic-content", "content-items"]})
    content_item = contents.find_all("div", {"class": "content-item"})
    import re
    regexp_img_1 = re.compile(r'https://dw8stlw9qt0iz\.cloudfront\.net/(.*?)\.png\"')
    text = soup.findAll(lambda tag: tag.name == 'div' and tag.get('class') == ['embedded-text-content'])
    t = text[:]
    texts = [text.p.text for text in t]
    text_1 = ""
    count = 0
    max_index = len(texts) - 1
    while count <= max_index:
        text_1 += texts[count] + '\n' + '\n'
        count += 1
    for item in content_header:
        try:
            if page.find("div", {"class", "topic-tags"}).text is not None:
                tags = page.find("div", {"class", "topic-tags"}).text
        except AttributeError:
            tags = None
        img_1_href = re.findall(regexp_img_1, item.find('style').text)
        try:
            video_1_data_scr = \
                contents.find("div", {"class": "first-video"}).find("div", {"class": "module-video"}).find("div", {
                    "class": "js-media-player"})["data-src"]
        except Exception as e:
            logger.exception(msg=f"Ошибка парсера: ссылка на видео не найдена - {e}")
            video_1_data_scr = None
        if item.find("div", {"class": "header-content"}).find('a') != None:
            channel = item.find("div", {"class": "header-content"}).find('a').text
            title = item.find("div", {"class": "header-content"}).find('h1').text
        elif item.find("div", {"class": "header-content"}).find('a') == None:
            channel = item.find("div", {"class": "header-content"}).find('h5').text
            title = item.find("div", {"class": "header-content"}).find('h1').text
    try:
        return img_1_href, channel, title, text_1, video_1_data_scr, tags, html
    except Exception as e:
        logger.exception(msg=f"Ошибка парсера: {e}")
        return img_1_href, channel, title, text_1, video_1_data_scr, tags, html

def translater(channel, title, text_1, tags):
    channel = {
        "key": "trnsl.1.1.20170730T114755Z.994753b77b648f24.f3ed7d2f59fcb232c089a1a3328c0e0b900d4925",
        "text": f"{channel}.",
        'lang': 'en-ru',
        'format': 'plain'
    }
    title = {
        "key": "trnsl.1.1.20170514T220842Z.5b2c14ecd7990670.3ccb355751262f1359f3c3ff0b9b7d5447ce39a1",
        "text": f"{title}.",
        'lang': 'en-ru',
        'format': 'plain'
    }
    text_1 = {
        "key": "trnsl.1.1.20170514T220842Z.5b2c14ecd7990670.3ccb355751262f1359f3c3ff0b9b7d5447ce39a1",
        "text": f"{text_1}.",
        'lang': 'en-ru',
        'format': 'plain'
    }
    if tags is not None:
        tags = {
            "key": "trnsl.1.1.20170514T220842Z.5b2c14ecd7990670.3ccb355751262f1359f3c3ff0b9b7d5447ce39a1",
            "text": f"{tags}",
            'lang': 'en-ru',
            'format': 'plain'
        }
    else:
        tags = {
            "key": "trnsl.1.1.20170514T220842Z.5b2c14ecd7990670.3ccb355751262f1359f3c3ff0b9b7d5447ce39a1",
            "text": f"Любопытно",
            'lang': 'en-ru',
            'format': 'plain'
        }
    tags_ru = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate', params=tags).json()
    channel_ru = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate', params=channel).json()
    title_ru = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate', params=title).json()
    text_1_ru = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate', params=text_1).json()
    channel_ru = channel_ru['text'][0]
    title_ru = title_ru['text'][0]
    text_1_ru = text_1_ru['text'][0]
    tags_ru = tags_ru['text'][0]
    logger.info("Переводчик выполнил свою работу")
    return tags_ru, channel_ru, title_ru, text_1_ru

def parse_post(href):
    root_logger = get_logs()
    root_logger.info('='*100)
    post_slug = href.replace('http://webcache.googleusercontent.com/search?q=cache:3XI5iWomPXMJ:http://curiosity.com/topics/', '').replace('/&strip=0&vwsrc=1', '')
    logger.info(f"Работа с постом {post_slug}")
    img_1_href, channel, title, text_1, video_1_data_scr, tags, html = parser(href)
    tags_ru, channel_ru, title_ru, text_ru = translater(channel, title, text_1, tags)
    tags_ru = tags_ru.replace(" ", "")
    tags_ru = tags_ru.split("\n")
    tags_ru = [tag for tag in tags_ru if len(tag) >= 2]
    text_ru = text_ru.replace("\n\n\n", "\n", 1)
    return img_1_href, post_slug, tags_ru, channel_ru, title_ru, text_ru, html, href

def updatedb(request):
    count_request = 0
    myposts = [post for post in Post.objects.all()]
    path_to_db = read_db(f"{os.path.dirname(os.path.abspath(__file__))}/parser/my_href_backup.db")
    hrefs = checkposts(myposts, path_to_db)
    l.info(f"Доступно {len(hrefs)} новых постов.")
    for href in hrefs:
        try:     
            img_1_href, post_slug, tags_ru, channel_ru, title_ru, text_ru, html, href = parse_post(href)
            l.warning(f"Хуячим пост {post_slug}")
            post = Post.objects.get_or_create(title=title_ru,
                                              html=html,
                                              url=href,
                                              slug=post_slug,
                                              text=text_ru,
                                              channel=check_channel(channel_ru))[0]
            post.save()
            add_tags(post=post, tags=tags_ru)
            post.save()
            create_image(href=img_1_href, post=post)
            add_image(
                post=post,
                img_href=img_1_href,
                channel=channel_ru,
                title=title_ru
                )
            if count_request == 2:
                break
            else:
                continue
        except Exception as err:
            l.error(err)
            continue

    return HttpResponseRedirect("/curiosity")

def trash():
    
    HOW_POST_TO_PRINT = 5
    VK_TOKEN = models.CharField(max_length=500, null=True, default="9bfae56722ff872d603c6b0aa10c9c47f42fa00de836de4e47217e44c7f06259767efb6ee95c494303a8e")
    PATH_TO_LOG = models.CharField(max_length=500, null=True, default=os.path.dirname(os.path.abspath(__file__)) + "parser/curiosity-to-vk.log")
    PATH_MY_HREF = models.CharField(max_length=500, null=True, default=os.path.dirname(os.path.abspath(__file__)) + "parser/my_href.db")
    PATH_TO_BACKUP_HREF = models.CharField(max_length=500, null=True, default=os.path.dirname(os.path.abspath(__file__)) + "parser/my_href_backup.db")
    PATH_TO_IMG_RESIZE = models.CharField(max_length=500, null=True, default=os.path.dirname(os.path.abspath(__file__)) + "parser/topics/IMG_RESIZE.png")
    PATH_TO_IMG_ORIGINAL = models.CharField(max_length=500, null=True, default=os.path.dirname(os.path.abspath(__file__)) + "parser/topics/IMG_ORIGINAL.png")
    # PATH_TO_IMG_1_COMPOSITE = models.CharField(max_length=500, null=True, default=os.path.dirname(os.path.abspath(__file__)) + "parser/topics/IMG_COMPOSITE.png")
    PATH_TO_IMG_LOGO_PAINTER = models.CharField(max_length=500, null=True, default=os.path.dirname(os.path.abspath(__file__)) + "parser/desing/logo-painter.png")
    PATH_TO_FONTS = models.CharField(max_length=500, null=True, default=os.path.dirname(os.path.abspath(__file__)) + "parser/topics/Roboto-Fonts/Roboto-Bold.ttf")
    PATH_TO_IMG_BUTTON = models.CharField(max_length=500, null=True, default=os.path.dirname(os.path.abspath(__file__)) + "parser/Button.png")
    VK_GROUP_ID = models.CharField(max_length=500, null=True, default=181925964)
    UUID4_HEX_REGEX = models.CharField(max_length=500, null=True, default=re.compile('[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}\Z', re.I))
    return


from project.apps.curiosity.parser.curiosity_one_post import *
from project.apps.curiosity.models import PostAuthor, Post, PostComment
import requests
import datetime
from django.shortcuts import get_object_or_404


FIRST_POST_INDEX = 21
TIMEOUT = 100


class PageParser:
    """Парсер списка постов"""

    url = None
    html = None
    soup = None
    cards = None

    def __init__(self, *args, **kwargs):
        if kwargs is not None: self.url = kwargs["url"]
        with open(file=str(os.path.dirname(os.path.abspath(__file__)) + '/parser/topics/discovery.html'), encoding="utf-8",
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
            res = requests.get(url_prefix + url_sufix, "b")
            with open(str(os.path.dirname(os.path.abspath(__file__)) + "/static/curiosity/img/" + self.article_slug + ".png"), 'wb') as zero:
                zero.write(res.content)
        else:
            print("Ошибка загрузки изображения")
        print("Скачены изображениея")


def get_html(html):
    clean_html = ""
    for p in [t for t in html.contents[1:len(html.contents)-4]]:
        clean_html += str(p)
    return clean_html


def post_maker(request):
    pp = PageParser(url=None)
    ci = CardIter(data=pp.cards)
    count = 0
    for c in ci:
        count = count + 1
        if count <= FIRST_POST_INDEX:
            continue
        result = False
        while not result:
            try:
                cp = CardParser(card=c)
                cp.format_text()
                p = Post.objects.get_or_create(
                    title=cp.card_title,
                    slug=cp.article_slug,
                    status="Опубликован",
                    html=get_html(cp.topic_container),
                    url="http://www.discoverychannel.ru/articles/" + cp.article_slug,
                    text = cp.text,
                    )[0]
                p.save()
                author = PostAuthor.objects.get(id=request.user.id)
                author.post_set.add(p)
                p.channel = Channel.objects.get(id=2)
                add_tags(post=p, tags=["Популярная наука", "Обыкновенные герои"])
                p.save()
                cp.img_downloader()
                draw_img_temp_path = draw(channel_ru=cp.card_title, title_ru="Power by@vo0doo", img_path=str(os.path.dirname(os.path.abspath(__file__)) + "/static/curiosity/img/" + cp.article_slug + ".png"))
                img = File(open(draw_img_temp_path, "rb"))
                p.fimg.save(draw_img_temp_path, img, save=True)
                print(f"{count}")
                img.close()
                p.save()
                break
            except Exception as err:
                logger.error(err)
                result = False
                break
        time.sleep(10)
        continue