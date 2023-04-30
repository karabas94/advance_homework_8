from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'short_description', 'author', 'created_at', 'is_draft']
    raw_id_fields = ('author',)
    list_filter = ['created_at']
    date_hierarchy = 'created_at'
    list_per_page = 50
    search_fields = ['author']


@admin.action(description='Mark selected comments as published')
def check_comment(modeladmin, request, queryset):
    for obj in queryset:
        obj.is_reviewed = True
        obj.save()


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'message', 'is_reviewed']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'
    list_per_page = 50
    search_fields = ['message']
    actions = [check_comment]
