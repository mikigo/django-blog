from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.urls import reverse
from django.utils.html import format_html

from .adminforms import PostAdminForm
from .models import Category
from .models import Post
from .models import Tag


class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1、自动补充文章、分类、标签、侧边栏、友链这些Model的owner字段
    2、针对queryset过滤当前用户的数据
    """
    exclude = ("owner",)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(owner=request.user)


class PostInline(admin.TabularInline):
    fields = ("title", "desc")
    # 控制额外多几个
    extra = 1
    model = Post


@admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ("name", "status", "is_nav", "created_time", "post_count")
    fields = ("name", "status", "is_nav")

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = "文章数量"


@admin.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ("name", "status", "created_time")
    fields = ("name", "status")


class CategoryOwnerFilter(admin.SimpleListFilter):
    title = "分类过滤器"
    parameter_name = "owner_category"

    # 返回要展示的内容和查询用的ID
    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list("id", "name")

    # 根据URL Query的内容返回列表页数据
    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


@admin.register(Post)
class PostAdmin(BaseOwnerAdmin):
    # 文章描述字段能够以 textarea（多行多列） 展示
    form = PostAdminForm
    # 配置列表页面展示哪些字段
    list_display = ("title", "category", "status", "created_time", "owner", "operator")
    # 配置哪些字段可以作为链接，点击他们，可以进入编辑页面，如果设置为None，表示不配置任何可点击的字段
    list_display_links = []
    # 配置页面的过滤器，需要通过哪些字段来过滤列表页
    # list_filter = ["category"]
    list_filter = [CategoryOwnerFilter]
    # 配置搜索字段
    search_fields = ["title", "category__name"]
    # 是否展示在顶部
    actions_on_top = True
    # 是否展示在底部
    actions_on_bottom = True
    # 保存、编辑、编辑并新建是否在顶部展示
    save_on_top = True
    # 限定要展示的字段，配置展示字段的顺序
    # fields = ("category", "title", "desc", "status", "content", "tag")
    # 控制页面布局
    fieldsets = (
        (
            "基础配置", {
                "description": "基础配置描述",
                "fields": (
                    ("title", "category"),
                    "status"
                )
            }
        ),
        (
            "内容", {
                "fields": (
                    "desc",
                    "content",
                    "content_ck",
                    "content_md",
                    "is_md",
                )
            }
        ),
        (
            "额外信息", {
                "classes": ("wide",),
                "fields": ("tag",)
            }
        )
    )
    # filter_vertical = ("tag",)

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = "操作"


# 日志
@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ["object_repr", "object_id", "action_flag", "user", "change_message"]
