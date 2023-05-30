from rest_framework import viewsets

from .models import Post
from .serializer import PostSerializer

# class PostViewSet(viewsets.ModelViewSet):
# 没有从前端写入的需求，ReadOnlyModelViewSet
class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    serializer_class = PostSerializer