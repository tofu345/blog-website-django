from django.contrib import admin

from api.models import Post, User


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content',
                    'author', 'updated', 'created']
    search_fields = ['title', 'author']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'image', 'is_staff', 'date_joined']
    search_fields = ['username', 'email']
