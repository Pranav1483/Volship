from django.urls import path
from . import views

urlpatterns = [
    path("signup/<str:email>", views.signup, name="signUp"),
    path("user/", views.getUser, name="getUser"),
    path("user/<int:id>", views.deleteUser, name="deleteUser"),
    path("post/", views.uploadPost, name="uploadPost"),
    path("post/<int:id>", views.editCaption, name="editCaption"),
    path("post/delete/<int:id>", views.deletePost, name='deletePost'),
    path("user/post/", views.getUserPosts, name="getUserPosts"),
    path("feed/latest/", views.getFeedPostsLatest, name="latestPosts"),
    path("feed/next/", views.getFeedPostsNext, name="nextPostSet")
]