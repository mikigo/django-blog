from django.contrib.admin import AdminSite

class CustomSite(AdminSite):
    site_header = "Typeidea"
    site_title = "Typeidea 管理后台"
    index_title = "youqu"

custom_site = CustomSite(name="cus_admin")