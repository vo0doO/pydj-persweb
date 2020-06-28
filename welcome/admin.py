from django.contrib import admin

from welcome.models import PageView, WelcomePage, WelcomePageBlock


# Register your models here.
class WelcomePageInline(admin.TabularInline):
    model = WelcomePage

    def __str__(self):
        return f"{self.id}"

class PageViewAdmin(admin.ModelAdmin):
    list_display = ['ip', 'hostname', 'timestamp']


class WelcomePageBlockAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'subtitle', 'link_text', "link_url"]
    inline = [WelcomePageInline]

class WelcomePageAdmin(admin.ModelAdmin):
    pass

admin.site.register(PageView, PageViewAdmin)
admin.site.register(WelcomePageBlock, WelcomePageBlockAdmin)
admin.site.register(WelcomePage, WelcomePageAdmin)
