from django.contrib import admin

from api.models import Post

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'author', 'updated', 'created']
    search_fields = ['title', 'author']
