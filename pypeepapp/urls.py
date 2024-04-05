from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list/', views.profile_list, name="profile_list"),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_password/', views.update_password, name='update_password'),
    path('profile/', views.my_profile, name='my_profile'),
    path('peep_like/<int:pk>', views.peep_like, name="peep_like"),
    path('peep_show/<int:pk>', views.peep_show, name="peep_show"),
]
