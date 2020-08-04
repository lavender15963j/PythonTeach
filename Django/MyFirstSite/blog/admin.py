from django.contrib import admin

from blog.models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'createTime',] # 顯示欄位

admin.site.register(Article, ArticleAdmin)
