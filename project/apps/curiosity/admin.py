from django.contrib import admin
import re
from django.contrib import messages
from django.contrib.admin import helpers
from django.contrib.admin.utils import get_deleted_objects, model_ngettext
from django.core.exceptions import PermissionDenied
from django.db import router
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy
from project.apps.curiosity.models import Channel, Image, Log, Post, Tag, PostAuthor, PostComment
from bs4 import BeautifulSoup
from django.contrib import messages


class PostInline(admin.TabularInline):
    model = Post


class PostCommentsInline(admin.TabularInline):
    model = PostComment


@admin.register(Channel)
class AdminChannel(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'created_date', 'like',)
    list_filter = ('created_date', 'like',)
    inlines = [PostInline]


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'created_date', 'like',)
    list_filter = ('created_date', 'like',)
    inline = [PostInline]


@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    fieldsets = (
        ('Действия', {'fields': ('author', 'created_date', )}),
        ('Содержание', {'fields': ('title', 'text', 'html', 'img',)}),
        ("Связи", {'fields': ('channel', 'tags',)}),
        ("Свойства", {'fields': ('status', 'url', 'slug',)}),
        )
    search_fields = ('title', 'text',)
    ordering = ('-status',)
    list_display = ('title', 'channel', 'display_tag', 'created_date', 'display_image',  'status', 'author')
    list_filter = ('channel', 'tags', 'status', 'created_date',  'rewrite_date',)
    filter_horizontal = ()
    inlines = [PostCommentsInline]
    list_per_page=10
    actions=['clean_img_tag', 'clean_h_tag',]

    def clean_img_tag(self, request, queryset):
        if not (1 > queryset.count()):
            if not queryset[0].clean_img_tag():
                self.message_user(request, "!!!!!!!!!!", messages.ERROR)
            elif not Post.objects.get(slug=p.slug).clean_img_tag(p):
                self.message_user(request, "!!!!!!!!!!", messages.WARNING)
            elif Post.objects.get(slug=p.slug).clean_img_tag():
                self.message_user(request, "!!!!!!!!!!", messages.SUCCESS)
        return lambda p: clean_img_tag(modeladmin, request, queryset), range(1, len(queryset))
    clean_img_tag.short_description = ugettext_lazy("Причесать теги с изображениями в выбраных постах %(verbose_name_plural)s")

    def clean_h_tag(self, request, queryset):
        if not (1 > queryset.count()):
            if not queryset[0].clean_h_tag():
                self.message_user(request, "!!!!!!!!!!", messages.ERROR)
            elif not Post.objects.get(slug=p.slug).clean_h_tag(p):
                self.message_user(request, "!!!!!!!!!!", messages.WARNING)
            elif Post.objects.get(slug=p.slug).clean_h_tag():
                self.message_user(request, "!!!!!!!!!!", messages.SUCCESS)
        return lambda p: clean_h_tag(modeladmin, request, queryset), range(1, len(queryset))
    clean_h_tag.short_description = ugettext_lazy("Причесать теги с заголовками в выбраных постах %(verbose_name_plural)s")


@admin.register(Image)
class AdminImage(admin.ModelAdmin):
    list_display = ('created_time', 'id', 'url',)
    list_filter = ('created_time',)


@admin.register(Log)
class AdminLog(admin.ModelAdmin):
    list_display = ('text', 'created_at',)
    list_filter = ('created_at',)
    search_fields = ('text',)
    ordering = ('created_at',)
    filter_horizontal = ()


@admin.register(PostAuthor)
class AdminPostAuthor(admin.ModelAdmin):
    list_display = ('user', 'bio',)
    list_filter = ('user', 'bio',)
    search_fields = ('user', 'bio',)
    filter_horizontal = ()
    inlines = [PostInline]


@admin.register(PostComment)
class AdminPostComment(admin.ModelAdmin):
    list_display = ('author', 'post', 'post_date')
    list_filter = ('author', 'post', 'post_date')
    search_fields = ('author', 'post', 'post_date')
    filter_horizontal = ()