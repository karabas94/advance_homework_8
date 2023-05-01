from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import RegisterForm, CommentForm, ContactFrom
from .models import Post
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .tasks import send_mail as contact_send_mail
from django.db.models import Count, Q
from django.core.paginator import Paginator

User = get_user_model()


def index(request):
    return render(request, 'index.html')


class RegisterFormView(generic.FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy("blog:post_list")

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
                return redirect("blog:post_list")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="registration/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("blog:post_list")


class UpdateProfile(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'registration/update_profile.html'
    success_url = reverse_lazy('blog:post_list')
    success_message = 'Profile updated'

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class UserProfile(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'registration/profile.html'

    def get_object(self, queryset=None):
        return self.request.user


class PublicProfile(generic.DetailView):
    model = User
    template_name = 'registration/public_profile.html'

    def get_object(self, queryset=None):
        user = User.objects.get(pk=self.kwargs['pk'])
        return user

    # signal(send mail to admin)


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'short_description', 'text', 'image', 'is_draft', ]
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'short_description', 'text', 'image', 'is_draft']
    success_url = reverse_lazy('blog:post_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(author=self.request.user)
        return queryset


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(author=self.request.user)
        return queryset


class PostListView(generic.ListView):
    model = Post
    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('author').annotate(
            comment_count=Count('comments', filter=Q(comments__is_reviewed=True))).all()
        queryset = queryset.order_by('created_at')
        username = self.kwargs.get('user')
        if username:
            queryset = queryset.filter(author__username=username)
        return queryset


class PostDetailView(generic.DetailView):
    model = Post
    queryset = Post.objects.select_related('author').all()
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(num_posts=Count('author__post'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = self.object.comments.filter(is_reviewed=True)
        paginator = Paginator(comments, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['comments'] = page_obj
        return context


# signal(send mail to admin)
def add_comment(request, pk):
    post = Post.objects.get(pk=pk)
    comments = post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})


@login_required
def my_draft(request):
    drafts = Post.objects.filter(author=request.user, is_draft=True)
    return render(request, 'blog/user_draft_post_list.html', {'drafts': drafts})


@login_required
def my_post(request):
    posts = Post.objects.filter(author=request.user, is_draft=False)
    return render(request, 'blog/user_my_post_list.html', {'posts': posts})


def contact_form(request):
    if request.method == "POST":
        form = ContactFrom(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            contact_send_mail.delay(subject, message, email)
            messages.add_message(request, messages.SUCCESS, 'Message sent')
            return redirect('blog:contact')
    else:
        form = ContactFrom()
    return render(request, "blog/contact.html", {"form": form})
