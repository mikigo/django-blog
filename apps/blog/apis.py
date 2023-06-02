from rest_framework import viewsets

from .models import Post, Category, Tag
from .serializer import PostSerializer, PostDetailSerializer, CategorySerializer, TagSerializer

# class PostViewSet(viewsets.ModelViewSet):
# 没有从前端写入的需求，ReadOnlyModelViewSet
class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    serializer_class = PostSerializer
    
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostDetailSerializer
        return super(PostViewSet, self).retrieve(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        """获取某个分类下的文章列表"""
        category_id = self.request.query_params.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)
    serializer_class = CategorySerializer

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.filter(status=Tag.STATUS_NORMAL)
    serializer_class = TagSerializer