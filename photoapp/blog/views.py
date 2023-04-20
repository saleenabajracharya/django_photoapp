from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from blog.models import Post
from django.shortcuts import render

# def home(request):
#     context = {
#         'posts' : Post.objects.all()
#     }
#     return render(request,'home.html',context)

def about(request):
    return render(request,'about.html',{'title': "About Page"})



class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = ["-date_posted"]
     
    



    

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title',  'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # def test_func(self):
    #     post = self.get_object()
    #     if self.request.user == post.author:
    #         return True
    #     return False

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title',  'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    

def search(request):
        query = request.GET['query']
        allPosts = Post.objects.filter(title__icontains=query).order_by("-date_posted")
        params = {'posts': allPosts, 'query':query}
        return render(request, 'search.html', params)


def Post(request):
    if request.method == 'POST':
        form = Post(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded image
            pass
    else:
        form = Post()

    context = {
        'form': form,
    }

    return render(request, 'post_form.html', context)