"""Django Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from apps.blog.views import IndexView, CategoryView, TagView, PostDetail, SearchView, AuthorView
from apps.comment.views import CommentView
from apps.config.views import LinkListView

# from apps.blog.views import post_list, post_detail

urlpatterns = [
    url(r"^$", IndexView.as_view(), name="index"),
    url(r"^category/(?P<category_id>\d+)/$", CategoryView.as_view(), name="category"),
    url(r"^tag/(?P<tag_id>\d+)/$", TagView.as_view(), name="tag"),
    url(r"^post/(?P<post_id>\d+).html$", PostDetail.as_view(), name="detail"),
    url(r"^search/$", SearchView.as_view(), name="search"),
    url(r"^author/(?P<owner_id>\d+)/$", AuthorView.as_view(), name="author"),
    url(r"links/$", LinkListView.as_view(), name="links"),
    url(r"comment/$", CommentView.as_view(), name="comment"),

    url(r'^admin/', admin.site.urls, name="admin"),
]
