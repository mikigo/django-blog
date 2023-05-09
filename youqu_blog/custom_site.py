from django.contrib.admin import AdminSite

class CustomSite(AdminSite):
    site_header = "youqu_blog"
    site_title = "youqu_blog 管理后台"
    index_title = "youqu_blog"

custom_site = CustomSite(name="cus_admin")