from django.conf.urls import include, url

from project.apps.curiosity import views

app_name = "curiosity"

# Curiosity Functions
urlpatterns = [
    url(r'^posts/get/file$', views.post_maker, name='post_maker'),
    url(r'^authors/(?P<pk>[-id]+)/posts/list/$', views.PostByAuthorListView.as_view(), name="author-post-list"),
    url(r'^channels/(?P<id>[-\w]+)/posts/list/$', views.PostByChannelListView.as_view(), name="channel-posts"),
    url(r'^tags/(?P<pk>[-\w]+)/posts/list/$', views.PostByTagListView.as_view(), name="tag-posts"),
]


# Posts Generic
urlpatterns += [
    url(r'^$', views.index, name='index'),
    url(r'^posts/$', views.PostListView.as_view(), name='post-list'),
    url(r'^posts/create/$', views.PostCreateView.as_view(), name='post-create'),
    url(r'^posts/(?P<slug>[-\w]+)/$', views.PostDetailView.as_view(), name="post-detail"),
    url(r'^posts/(?P<slug>[-\w]+)/update/$', views.PostUpdateView.as_view(), name="post-change"),
    url(r'^posts/(?P<slug>[-\w]+)/delete/$', views.PostDeleteView.as_view(), name="post-delete"),
]

# Tags Generic
urlpatterns += [
    url(r'^tags/$', views.TagListView.as_view(), name='tag-list'),
    url(r'^tags/create/$', views.TagCreateView.as_view(), name='tag-create'),
    url(r'^tags/(?P<pk>[-\w]+)/$', views.TagDetailView.as_view(), name="tag-detail"),
    url(r'^tags/(?P<pk>[-\w]+)/update/$', views.TagUpdateView.as_view(), name="tag-change"),
    url(r'^tags/(?P<pk>[-\w]+)/delete/$', views.TagDeleteView.as_view(), name="tag-delete"),
]

# Channels Generic
urlpatterns += [
    url(r'^channels/$', views.ChannelListView.as_view(), name='channel-list'),
    url(r'^channels/create/$', views.ChannelCreateView.as_view(), name='channel-create'),
    url(r'^channels/(?P<pk>[-\w]+)$/$', views.ChannelDetailView.as_view(), name="channel-detail"),
    url(r'^channels/(?P<pk>[-\w]+)$/update/$', views.ChannelUpdateView.as_view(), name="channel-change"),
    url(r'^channels/(?P<pk>[-\w]+)$/delete/$', views.ChannelDeleteView.as_view(), name="channel-delete"),
]
