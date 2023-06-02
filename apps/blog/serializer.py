from rest_framework import serializers
from .models import Post, Category, Tag

class PostSerializer(serializers.HyperlinkedModelSerializer):

    category = serializers.SlugRelatedField(
        read_only=True,
        # 指定要展示的字段
        slug_field="name",
    )
    tag = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    url = serializers.HyperlinkedIdentityField(view_name="api-post-detail")

    class Meta:
        model = Post
        fields = [
            "url",
            "id",
            "title",
            "category",
            "tag",
            "owner",
            "created_time",
        ]

class PostDetailSerializer(PostSerializer):

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "category",
            "tag",
            "owner",
            "content",
        ]

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name", "created_time"]

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ["id", "name", "created_time"]