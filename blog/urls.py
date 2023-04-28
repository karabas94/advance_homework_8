from django.urls import path
from .views import PostCreateView, PostUpdateView, PostDeleteView, PostListView, PostDetailView, my_draft, my_post, add_comment

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),

    path('post/create/', PostCreateView.as_view(), name='post_form'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/', PostListView.as_view(), name='post_list'),
    path('post_by_<str:user>/', PostListView.as_view(), name='user_post_list'),

    path('my_post', my_post, name='user_my_post_list'),
    path('my_draft/', my_draft,  name='user_draft_post_list'),

    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/comment/', add_comment, name='add_comment'),
]
