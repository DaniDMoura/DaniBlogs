from django.urls import path
from .views import *

urlpatterns = [
    path("", post_list, name="post_list"),
    path("post/<slug:slug>/", post_detail, name="post_detail"),
    path("add/", add_page, name="add_post"),
    path("login/", login, name="login"),
    path("signup/", signup, name="signup"),
    path('logout/', logout_view, name='logout')
]
