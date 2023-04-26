from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import RegisterForm
from .models import Post
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

User = get_user_model()


def index(request):
    return render(request, 'index.html')


class RegisterFormView(generic.FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy("blog:index")

    def form_valid(self, form):
        user = form.save()
        user = authenticate(username=user.username, password=form.cleaned_data.get("password1"))
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("blog:index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="registration/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("blog:index")


class UpdateProfile(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'registration/update_profile.html'
    success_url = reverse_lazy('blog:index')
    success_message = 'Profile updated'

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class UserProfile(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'registration/profile.html'

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class PublicProfile(generic.DetailView):
    model = User
    template_name = 'registration/public_profile.html'

    def get_object(self, queryset=None):
        user = User.objects.get(pk=self.kwargs['pk'])
        return user


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'short_description', 'text', 'image', 'is_draft', 'is_published']
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'short_description', 'text', 'image', 'is_draft', 'is_published']
    success_url = reverse_lazy('blog:index')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(author=self.request.user)
        return queryset


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(author=self.request.user)
        return queryset


class PostListView(generic.ListView):
    model = Post

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.kwargs.get('user')
        if username:
            queryset = queryset.filter(author__username=username)
        return queryset


class PostDetailView(generic.DetailView):
    model = Post


@login_required
def my_draft(request):
    drafts = Post.objects.filter(author=request.user, is_draft=True)
    return render(request, 'blog/user_draft_post_list.html', {'drafts': drafts})


@login_required
def my_post(request):
    posts = Post.objects.filter(author=request.user, is_published=True)
    return render(request, 'blog/user_my_post_list.html', {'posts': posts})
