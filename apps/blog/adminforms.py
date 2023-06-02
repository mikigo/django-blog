from mdeditor.fields import MDTextFormField
from dal import autocomplete
from django import forms

from .models import Category, Tag, Post


class PostAdminForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=autocomplete.ModelSelect2(url="category-autocomplete"),
        label="分类",
    )
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
        label='标签',
    )

    desc = forms.CharField(widget=forms.Textarea(), label="摘要", required=False)
    content = MDTextFormField(label="正文", required=False)

    class Meta:
        model = Post
        fields = (
            # 自动补全的字段放在前面
            "category",
            "tag",
            "title",
            "desc",
            "content",
            "status",
        )
