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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import re_path
from django.urls import path
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from apps.blog.apis import PostViewSet, CategoryViewSet
from apps.blog.views import IndexView, CategoryView, TagView, PostDetail, SearchView, AuthorView
from apps.comment.views import CommentView
from apps.config.views import LinkListView
from .autocomplete import CategoryAutocomplete, TagAutocomplete

schema_view = get_schema_view(
    openapi.Info(
        title=settings.PROJECT_NAME,
        default_version="v1",
        description=settings.PROJECT_NAME,
        terms_of_service="",
        contact=openapi.Contact(email="xxxxx.com"),
        license=openapi.License(name="Apache License"),
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r"post", PostViewSet, basename="api-post")
router.register(r"category", CategoryViewSet, basename="api-category")

urlpatterns = [
    url(r"^$", IndexView.as_view(), name="index"),
    url(r"^category/(?P<category_id>\d+)/$", CategoryView.as_view(), name="category"),
    url(r"^tag/(?P<tag_id>\d+)/$", TagView.as_view(), name="tag"),
    url(r"^post/(?P<post_id>\d+).html$", PostDetail.as_view(), name="detail"),
    url(r"^search/$", SearchView.as_view(), name="search"),
    url(r"^author/(?P<owner_id>\d+)/$", AuthorView.as_view(), name="author"),
    url(r"^links/$", LinkListView.as_view(), name="links"),
    url(r"^comment/$", CommentView.as_view(), name="comment"),

    # api
    url(r"^api/", include((router.urls, "api"), namespace="api")),
    # 文档
    re_path(
      r"docs(?P<format>\.json|\.yaml)",
      schema_view.without_ui(cache_timeout=0),
      name="schema-json",
    ),
    path(
      "docs/",
      schema_view.with_ui("swagger", cache_timeout=0),
      name="schema-swagger-ui",
    ),
    # path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    # admin
    url(r'^admin/', admin.site.urls, name="admin"),

    # 自动补全
    url(r"^category-autocomplete/$", CategoryAutocomplete.as_view(), name="category-autocomplete"),
    url(r"^tag-autocomplete/$", TagAutocomplete.as_view(), name="tag-autocomplete"),
    url(r"^ckeditor/", include("ckeditor_uploader.urls")),
] \
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
