import mistune
from django.conf import settings
from django.db.models import Q
from django.views.generic import ListView, DetailView

# Create your views here.
from apps.blog.models import Tag, Post, Category
from apps.comment.forms import CommentForm
from apps.comment.models import Comment
from apps.config.models import SideBar


class CommonMixin:

    def get_category_context(self):
        categories = Category.objects.filter(status=1)

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
        sidebars = SideBar.objects.filter(status=1)
        recently_posts = Post.objects.filter(status=1)[:10]
        recently_comments = Comment.objects.filter(status=1)[:10]
        kwargs.update({
            'sidebars': sidebars,
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
    context_object_name = 'post_list'
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
    queryset = Post.latest_posts()
    # model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"
    pk_url_kwarg = "post_id"

    def get_context_data(self, **kwargs):
        """在detail.html模板中拿到comment_form和comment_list变量"""
        context = super().get_context_data(**kwargs)
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