from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse_lazy
from django.views import generic

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


# Create your views here.
from django.http import HttpResponse


from blog.models import Comment, Article

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.

@login_required
def index(request):
    return render(request, 'blog/index.html')
   
@method_decorator(login_required, name='dispatch')   
class IndexView(generic.TemplateView):
    template_name = 'blog/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['msg'] = "哈囉 %s" % self.request.user
        else:
            context['msg'] = "請先登入"
        return context
    
# blog/views.py

def login(request):
    if request.POST:
        # 當使用者 POST 表單後運行這部分程式碼
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 用 auth.authenticate 來找 db 內是否有這筆帳戶資料
        user = auth.authenticate(username=username, password=password)

        if user and user.is_active: # 判斷 user 是否存在，且沒有被凍結
            # 允許登入
            auth.login(request, user)
            return redirect(reverse_lazy('index')) # 進行導頁到 index(跟 template tag url 一樣，參數是剛剛在 urls.py 取的名稱)
        else:     
            # 不允許登入
            context = {
                "msg": "登入失敗",
            }
            return render(request, 'blog/login.html', context)
    
    return render(request, 'blog/login.html')
    
class LoginView(generic.View):

    # get function 裡面寫 get 時要處理的事
    def get(self, request, *args, **kwargs):
        return render(request, 'blog/login.html')

    # post function 裡面寫 post 時要處理的事
    def post(self, request, *args, **kwargs):
        # 當使用者 POST 表單後運行這部分程式碼
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 用 auth.authenticate 來找 db 內是否有這筆帳戶資料
        user = auth.authenticate(username=username, password=password)
        
        if user and user.is_active: # 判斷 user 是否存在，且沒有被凍結
            # 允許登入
            auth.login(request, user)
            return redirect(reverse_lazy('index')) # 進行導頁到 index
        else:     
            # 不允許登入
            context = {
                "msg": "登入失敗",
            }
            return render(request, 'blog/login.html', context)
    
def logout(request):
    auth.logout(request)
    return redirect(reverse_lazy('index'))
    
def register(request):
    if request.POST:
        # 當使用者 POST 表單後運行這部分程式碼
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if not User.objects.filter(username=username).exists(): # 判斷是否 username 有存在 db 內
                user = User.objects.create(
                    username=username,
                    password=make_password(password1), # 密碼加密
                )
                return redirect(reverse_lazy('login'))  # 登出後導頁到 login
            else:
                context = {
                    "msg": "此使用者帳號已被申請過",
                }
                return render(request, 'blog/register.html', context)
        else:
            context = {
                "msg": "一次密碼與二次密碼不相同",
            }
            return render(request, 'blog/register.html', context)
    return render(request, 'blog/register.html')


def page1(request):
    if request.POST:  # 判斷是否是 POST
        name = request.POST.get("name")
        content = request.POST.get("content")
        
        comment = Comment.objects.create(  # 在 db 內新增一筆 Comment
            name=name,
            content=content,
        )
        
    context = {
        "comments": Comment.objects.filter(name='AAA'), # select * from Comment;
    }
    return render(request, 'blog/page1.html', context)
    
from blog.forms import ArticleForm

def createArticle(request):
    context = {}
    
    if request.POST:
        form = ArticleForm(request.POST)
        if form.is_valid():
            # 表單符合規則
            # 用 POST 的資料做成一個 article 物件(相當於 Article.objects.create)
            # commit=False 表示先別直接紀錄到 db，因為我們還要加其他資料
            article = form.save(commit=False) 
            article.author = request.user # 紀錄是誰 create 這個 article 的
            article.save() # 紀錄到 db 去

            context['msg'] = "成功新增一篇文章"
        else:
            # 表單不符合規則
            context['msg'] = "表單錯誤"
    else:
        form = ArticleForm()

    context['form'] = form
        
    return render(request, 'blog/article-add.html', context)
    
    
def articleList(request):
    context = {
        "articles": Article.objects.all(),
    }
    return render(request, 'blog/article-list.html')
    
    
class ArticleList(generic.ListView):
    template_name = 'blog/article-list.html' # 用來 render 的 template 
    context_object_name = 'articles' # 傳給 template 的 context 名稱
    paginate_by = 4

    def get_queryset(self): # 拿取一堆資料(list)
        return Article.objects.all()

class ArticleDetail(generic.DetailView):
    template_name = 'blog/article-detail.html' # 用來 render 的 template 
    context_object_name = 'article' # 傳給 template 的 context 名稱

    def get_object(self, queryset=None): # 依照傳入的資料，拿取單一一筆資料
        pk = self.kwargs.get("pk")
        return Article.objects.get(id=pk)
        
class ArticleCreateView(generic.FormView):
    form_class =  ArticleForm
    template_name = 'blog/article-add.html'
    success_url = reverse_lazy('article-list') # redirect 到哪個 url

    def form_valid(self, form):
        # 表單符合規則
        # 用 POST 的資料做成一個 article 物件(相當於 Article.objects.create)
        # commit=False 表示先別直接紀錄到 db，因為我們還要加其他資料
        article = form.save(commit=False) 
        article.author = self.request.user # 紀錄是誰 create 這個 article 的
        article.save() # 紀錄到 db 去

        return super().form_valid(form)

    # 可不寫
    def form_invalid(self, form):
        # 表單不符合規則
        # do something
        return super().form_invalid(form)
        
class ArticleCreateView(generic.CreateView):
    template_name = 'blog/article-add.html'
    success_url = reverse_lazy('article-add')
    
    form_class =  ArticleForm
    # model = Article
    # fields = ['title', 'content',]

    def form_valid(self, form):
        article = form.save(commit=False) 
        article.author = self.request.user 
        article.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
        
from django.contrib import messages

class ArticleUpdateView(generic.UpdateView):
    model = Article # 想更新的 Model
    template_name = 'blog/article-update.html'
    form_class = ArticleForm  # 更新時使用的 Form
    
    def form_valid(self, form): # 表單成功
        messages.success(self.request, '成功更新了文章') # message
        return super().form_valid(form)

    def form_invalid(self, form): # 表單失敗
        messages.error(self.request, '表單填寫錯誤') # message
        return super().form_invalid(form)

    def get_success_url(self):  # 更新完後，指定回傳的頁面
        # 我這邊指定回去 Detail 頁
        return reverse_lazy('article-detail', kwargs={'pk': self.object.id,})

class ArticleDeleteView(generic.DeleteView):
    model = Article # 想刪除的 Model
    success_url = reverse_lazy('article-list') # 刪除此 Article 後，指定回傳的頁面
    template_name = 'blog/article-delete.html'