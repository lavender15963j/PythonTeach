from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Comment(models.Model): # 在 db 內新增 Comment 的 table
    # 不用建 id，id 自動會有
    name = models.CharField(max_length=50) # 新增一個 char(50) 的欄位 name
    name2 = models.CharField(max_length=50, null=True)
    content = models.TextField() # 新增一個 text 的欄位 cotent
    createTime = models.DateTimeField(auto_now_add=True) # 新增一個時間欄位，而當資料被 create 時，這筆資料的 createTime 會存當下的時間
    
class Article(models.Model):
    title = models.CharField(max_length=200)
    createTime = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    
    def __str__(self):
        return "%s by %s" % (self.title, self.author)