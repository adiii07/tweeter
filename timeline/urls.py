from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('createpost/', views.create_post, name="create_post"),
    path('signup/', views.signup, name="signup"),
    path('account/<str:username>', views.accounts, name="accounts"),
    path('account/<str:username>/following', views.following, name="following"),
    path('account/<str:username>/followers', views.followers, name="followers"),
    path('post/<int:post_id>/', views.post, name="post"),
    path('post/<int:post_id>/reply', views.new_reply, name="new_reply")
]