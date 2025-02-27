from django.contrib import admin
from .models import Post, Signup


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "date_published", "slug")
    search_fields = ("title", "content")


admin.site.register(Post, PostAdmin)


class SignupAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "username")
    search_fields = ("username", "first_name")


print(Signup)
admin.site.register(Signup, SignupAdmin)
