from django.contrib.admin import AdminSite

class CustomSite(AdminSite):
    site_header = "django_blog"
    site_title = "django_blog 管理后台"
    index_title = "django_blog"

custom_site = CustomSite(name="cus_admin")