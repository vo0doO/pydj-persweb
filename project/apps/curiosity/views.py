from django.shortcuts import get_object_or_404
import datetime
from project.apps.curiosity.models import PostAuthor, Post, PostComment
from project.apps.curiosity.parser.curiosity_one_post import *
import logging
import os
import sys
import time
import urllib
from urllib.parse import urlparse
import PIL
import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, View
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.core.files import File
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.contenttypes.models import ContentType
from authentication.models import CustomUser as User
from project.apps.curiosity.models import (Channel, Post, PostComment, Tag)
from project.apps.curiosity.models import Image as CImage
logger = logging.getLogger(__name__)
import django.contrib.admin.helpers as help
from django.contrib import messages

def get_logs():
    fmt = logging.Formatter(
        '%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s')

    file_handler = logging.FileHandler(filename=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "parser", "curiosity-to-vk.log"))
    file_handler.setFormatter(fmt)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(fmt)

    root_logger = logging.getLogger()

    root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)

    root_logger.setLevel(logging.INFO)
    return root_logger

l = get_logs()


from project.apps.curiosity.forms import PostCommentForm


def manage_comment(request, slug):
    post = Post.objects.get(slug=slug)
    if request.method == "POST":
        comment = PostComment.objects.create(post_id=post.id, author=request.user, post_date=datetime.datetime.now())
        form = PostCommentForm(request.POST, instance=comment) or None
        if form.is_valid():
            if (form.cleaned_data['description'] is not Null) and (len(form.cleaned_data['description']) > 1):
                comment.description = form.cleaned_data['description']
                comment.save()
                form.save()
                return HttpResponseRedirect(str("/curiosity/posts/" + str(post.slug) + "/"))
            else:
                messages.error(self.request, "Коментарий не должен быть пустым !")
                form = PostCommentForm()
                return render(request, 'curiosity/include/html/atom/comment_form.html', {'form': form})
        else:
            messages.error(self.request, "Что-то пошло не так !")
            form = PostCommentForm()
            return render(request, 'curiosity/include/html/atom/comment_form.html', {'form': form})
    else:
        form = PostCommentForm()
        return render(request, 'curiosity/include/html/atom/comment_form.html', {'form': form})


class PostListView(ListView):
    paginate_by = 8
    models = Post
    queryset = Post.objects.order_by('-created_date')
    context_object_name = 'post_list'
    template_name = "curiosity/post_list.html"


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

    paginate_by = 10


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

    paginate_by = 10


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

    paginate_by = 10


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



class PostByChannelListView(ListView):
    model = Post


class PostByTagListView(ListView):
    model = Post


class PostByAuthorListView(LoginRequiredMixin, ListView):
    models = Post
    query_pk_and_slug = True
    queryset = Post.objects.all()
    template_name = "curiosity/pubpost_list_author_user.html"

    paginate_by = 10

    def get_queryset(self):
        return self.queryset.filter(author_id=self.request.user.id)


def index(request):
    """Просмотр функции для главной страницы сайта."""

    # Сформировать подсчеты некоторых из основных объектов
    num_posts = Post.objects.all().count()
    num_channels = Channel.objects.all().count()

    # Опубликованные посты (status = 'a')
    num_pub = len([post.status for post in Post.objects.all()
                   if post.status == "Опубликован"])
    num_new = len([post.status for post in Post.objects.all()
                   if post.status == "Обнаружен"])
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


start_count, final_count = 101, 200
TIMEOUT = 100


class PageParser:
    """Парсер списка постов"""

    url = None
    html = None
    soup = None
    cards = None

    def __init__(self, *args, **kwargs):
        if kwargs is not None:
            self.url = kwargs["url"]
        with open(file=str(os.path.dirname(os.path.abspath(__file__)) + '/parser/topics/discovery.html'), encoding="utf-8",
                  mode="r") as f:
            self.html = f.read()
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
        self.card_title = card.find(
            "div", {"class": ["show-card__name title title_h4"]}).text
        self.article_slug = self.card_link[0].split('/')[2]
        self.article_page = requests.get(
            self.link_sufix + self.article_slug + "/")
        self.article_soup = BeautifulSoup(self.article_page.text, "lxml")
        self.topic_container = self.article_soup.find(
            "div", {"class": "topic__container container"})

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
        file_path = str(os.path.dirname(os.path.abspath(__file__)) + "/static/curiosity/img/" + self.article_slug + ".png")
        if url_sufix is not None:
            res = requests.get(url_prefix + url_sufix, "b")
            with open(file_path,'wb') as zero:
                zero.write(res.content)
        else:
            print("Ошибка загрузки изображения обложки")
        print("Скачено изображение обложки")


def get_html(html):
    clean_html = ""
    for p in [t for t in html.contents[1:len(html.contents)-4]]:
        clean_html += str(p)
    return clean_html

def get_all_img(html, p):
        topic_images = html.findAll({"img": "href"})
        count = 0
        for img in topic_images:
            count = count + 1
            res = requests.get(
                url_prefix + img["src"]
            )

            with open(
                str(os.path.dirname(os.path.abspath(__file__)) + "/static/curiosity/img/" + self.article_slug + "__" + img["src"].split("/")[-1]),'wb') as zero:
                    zero.write(res.content)

            image = CImage.objects.create(
                id=self.article_slug,
                urls_x300=img["alt"],
                url_prefix="http://io.net.ru:1443/img/",
                url_sufix=".jpg",
                role=str("б" + str(count)),)

            image.post_set.add(p)

            img["src"] = str(image.url_prefix + self.article_slug + "__" + img["src"].split("/")[-1])

def post_maker(request):

    pp = PageParser(url=None)
    ci = CardIter(data=pp.cards)
    count = 0

    for c in ci:

        result = False
        count = count + 1
        if count <= start_count:
            continue
        elif count >= final_count:
            break

        while not result:

            try:
                cp = CardParser(card=c)
                cp.format_text()
                
                cp.img_downloader()
                p = Post.objects.get_or_create(
                    title=cp.card_title,
                    slug=cp.article_slug,
                    status="Опубликован",
                    html=get_html(cp.topic_container).replace('src="/', 'src="http://www.discoverychannel.ru/'),
                    url="http://www.discoverychannel.ru/articles/" + cp.article_slug,
                    text=cp.text,
                )[0]
                p.save()

                author = PostAuthor.objects.get(id=request.user.id)
                author.post_set.add(p)

                p.channel = Channel.objects.get(id=2)

                add_tags(post=p, tags=[
                         "Популярная наука", "Обыкновенные герои"])
                p.save()
                draw_img_temp_path = draw(channel_ru=cp.card_title, title_ru="Power by@vo0doo", img_path=str(
                    os.path.dirname(os.path.abspath(__file__)) + "/static/curiosity/img/" + p.slug + ".png"))
                im = PIL.Image.open(draw_img_temp_path, "r")

                image = CImage.objects.create(
                    id=p.slug,
                    url_prefix="http://io.net.ru:1443/img/",
                    url_sufix=".jpg",
                    role=str("б" + str(count)),
                    )
                print(f"{count}")
                image.save()
                p.img = image
                im.close()
                p.save()
                break

            except Exception as err:
                logger.error(err)
                result = False
                break

        time.sleep(10)
        continue

from django.contrib.auth.decorators import login_required


