from django.shortcuts import render, get_object_or_404
# Login Required for PostCreateView - Class /post/new/, Only logged-in user can update post /post/7/update/
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from django.http import HttpResponse

# Used for testing before database connectivity - replaced with  Post.objects.all()
posts = [
    {
        "author": "Lawrence",
        "title": "Blog Post 1",
        "content": "First post content",
        "date_posted": "October 05, 2023",
    },
    {
        "author": "Marie",
        "title": "Blog Post 2",
        "content": "Second post content",
        "date_posted": "October 06, 2023",
    },
]


# Function Based View
def home(request):
    context = {"posts": Post.objects.all(), "title": "Home"}
    return render(request, "blog/home.html", context)


# Class Based Views
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


# Posts associated with a user
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    # Get user or 404 - get_object_or_404
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    # Assign author to the currently logged-in user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # check logged-in user is the owner of the post to update
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    # check logged-in user is the owner of the post to delete
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, "blog/about.html", {"title": "About"})
