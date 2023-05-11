from django.contrib import admin
from django.conf import settings

# Register your models here.
from .models import Link
from .models import SideBar

# simpleui的配置
admin.site.site_header = settings.PROJECT_NAME.title()
admin.site.site_title = settings.PROJECT_NAME.title()

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("title", "href", "status", "weight", "created_time")
    fields = ("title", "href", "status", "weight")

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)

@admin.register(SideBar)
class SideBarAdmin(admin.ModelAdmin):
    list_display = ("title", "display_type", "content", "created_time")
    fields = ("title", "display_type", "content")

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)
