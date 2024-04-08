from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list/', views.profile_list, name="profile_list"),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('profile/followers/<int:pk>', views.followers, name='followers'),
    path('profile/follows/<int:pk>', views.follows, name='follows'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_password/', views.update_password, name='update_password'),
    path('profile/', views.my_profile, name='my_profile'),
    path('peep_like/<int:pk>', views.peep_like, name="peep_like"),
    path('peep_show/<int:pk>', views.peep_show, name="peep_show"),
    path('unfollow/<int:pk>', views.unfollow, name="unfollow"),
    path('follow/<int:pk>', views.follow, name="follow"),   
    path('delete_peep/<int:pk>', views.delete_peep, name="delete_peep"),
    path('edit_peep/<int:pk>', views.edit_peep, name="edit_peep"),
    path('search/', views.search, name="search"),
    path('search_user/', views.search_user, name="search_user"),
]
