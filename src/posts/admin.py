from django.contrib import admin

# Register your models here.
from .models import Post

#Adding more field to post table like time,update
class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "updated", "timestamp"]
    list_display_links = ["updated"]
    list_filter = ["updated", "timestamp"]
    list_editable = ["title"]
    search_fields = ["title", "content"]

    class meta:
        model = Post

admin.site.register(Post, PostModelAdmin)
