import mistune
from django.conf import settings
from django.db.models import Q
from django.views.generic import ListView, DetailView

# Create your views here.
from apps.blog.models import Tag, Post, Category
from apps.comment.forms import CommentForm
from apps.comment.models import Comment
from apps.config.models import SideBar


# def post_list(request, category_id=None, tag_id=None):
#     tag = None
#     category = None
#
#     if tag_id:
#         post_list, tag = Post.get_by_tag(tag_id)
#     elif category_id:
#         post_list, category = Post.get_by_category(category_id)
#     else:
#         post_list = Post.latest_posts()
#
#     context = {
#         "category": category,
#         "tag": tag,
#         "post_list": post_list,
#         "sidebars": SideBar.get_all(),
#     }
#     # 把所有分类加进来
#     context.update(Category.get_navs())
#
#     return render(
#         request,
#         "blog/list.html",
#         context=context
#     )
#
#
# def post_detail(request, post_id):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         post = None
#
#     context = {
#         "post": post,
#         "sidebars": SideBar.get_all(),
#     }
#     return render(
#         request,
#         "blog/detail.html",
#         context=context
#     )


class CommonMixin:

    def get_category_context(self):
        categories = Category.objects.filter(status=1)  # TODO: fix magic number

        nav_cates = []
        cates = []
        for cate in categories:
            if cate.is_nav:
                nav_cates.append(cate)
            else:
                cates.append(cate)
        return {
            'nav_cates': nav_cates,
            'cates': cates,
        }

    def get_context_data(self, **kwargs):
        side_bars = SideBar.objects.filter(status=1)
        recently_posts = Post.objects.filter(status=1)[:10]
        recently_comments = Comment.objects.filter(status=1)[:10]
        kwargs.update({
            'side_bars': side_bars,
            'recently_comments': recently_comments,
            'recently_posts': recently_posts,
        })
        if settings.HOME_TITLE:
            kwargs.update({
                "home_title": settings.HOME_TITLE
            })
        if settings.POWER_BY:
            kwargs.update({
                "power_by": settings.POWER_BY
            })
        kwargs.update(self.get_category_context())
        return super(CommonMixin, self).get_context_data(**kwargs)


class BasePostsView(CommonMixin, ListView):
    model = Post
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 3
    allow_empty = True


class IndexView(BasePostsView):
    pass


class CategoryView(BasePostsView):

    def get_queryset(self):
        qs = super(CategoryView, self).get_queryset()
        cate_id = self.kwargs.get('category_id')
        qs = qs.filter(category_id=cate_id)
        return qs


class TagView(BasePostsView):

    def get_queryset(self):
        tag_id = self.kwargs.get('tag_id')
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            return []

        posts = tag.posts.all()
        return posts


class PostDetail(CommonMixin, DetailView):
    # queryset = Post.latest_posts()
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"
    pk_url_kwarg = "post_id"

    def get_context_data(self, **kwargs):
        """在detail.html模板中拿到comment_form和comment_list变量"""
        context = super().get_context_data()
        context.update({
            "comment_form": CommentForm,
            "comment_list": Comment.get_by_target(self.request.path)
        })
        # 转换为markdown
        context["post"].content = mistune.markdown(context["post"].content)
        return context


class SearchView(IndexView):

    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            "keyword": self.request.GET.get("keyword", "")
        })
        return context

    def get_queryset(self):
        queryseet = super().get_queryset()
        keyword = self.request.GET.get("keyword")
        if not keyword:
            return queryseet
        return queryseet.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class AuthorView(IndexView):

    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get("owner_id")
        return queryset.filter(owner_id=author_id)
