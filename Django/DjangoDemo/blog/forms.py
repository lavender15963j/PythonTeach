from django import forms

from blog.models import Article


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article  # 這個 form 指定給 Article 這個 model 用
        fields = ['title', 'content',] # 在表單上只做出 Article 的兩個欄位
        labels = {
            'title': "標題",
            'content': "內文",
        }
        
    def clean_title(self): # clean_[想要的欄位](self)
        title = self.cleaned_data['title'] # 拿到表單資料
        if not title.startswith("ZZZ"):
            raise forms.ValidationError("文章 title 開頭必須為 ZZZ")

        return title # 回傳 data
