from django.shortcuts import render
from django.http import HttpResponseRedirect
from app.models import Post, Comment
from django.utils import timezone
from app.forms import PostForm, CommentForm,RegisterForm

from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView,RedirectView)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm


class AboutView(TemplateView):
    template_name = 'blog/about.html'

class PostListView(ListView):
    model = Post
    template_name='blog/post_list.html'
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post
    template_name='blog/post_detail.html'
    
    



class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    template_name = 'blog/post_form.html'

    form_class = PostForm

    model = Post


class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm

    model = Post


class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    template_name = 'blog/post_list.html'

    model = Post
    form_class = PostForm

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    template_name='blog/post_confirm_delete.html'
    success_url=reverse_lazy('post_list')
    


class UserLoginView(AuthenticationForm):
   
   success_url=reverse_lazy('post_list')  

#######################################
## Functions that require a pk match ##
#######################################

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)



'''
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")    
'''

class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = 'http://127.0.0.1:8000/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


'''
def logout_view(request):
    logout(request)
    success_url=reverse_lazy('post_list')
    return HttpResponseRedirect('post_list')
'''   

def Login(request):
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['Password']
        user = authenticate(username=username, password=password)
        print("Password",password)
        if user is not None:
            if user.is_active:
                login(request, user)
                print(user.is_active)
                
                return redirect('post_list')
            else:
                print('else block')
                return redirect("Inactive user.")
        else:
            from django.contrib import messages 
            messages.add_message(request, messages.INFO, 'Check your User name or Password')
            return redirect('login')

    return render(request, "registration/login.html")        

'''
class UserRegisterView(CreateView):
    form_class= UserCreationForm
    
    template_name='registration/signup.html'
    success_url=reverse_lazy('post_list')

'''
def UserRegisterView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('post_list')
    else:
        form = RegisterForm()
    return render(request, 'registration/signup.html', {'form': form})    
