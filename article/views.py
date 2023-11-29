from django.views import generic
from .models import Post
from .forms import CreateArticleForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# the list of articles to show in articles page
class PostList(LoginRequiredMixin, generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'article.html'


# the details of every post
@login_required
def post_detail(request, pk):
    details = Post.objects.get(id=pk)
    return render(request, 'article_detail.html', {'details': details})


# creating post only by admins
@login_required
def article_plus(request):
    if request.method == "POST":
        form = CreateArticleForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the author field to the current user
            post.save()  # Save the post before redirecting
            return redirect('article:home')  # Replace 'article:home' with the actual URL or view name
    else:
        form = CreateArticleForm()

    return render(request, 'add_article.html', {'form': form})

