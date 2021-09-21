from django.urls import path
from user_profile import views


urlpatterns = [
    path('', views.UserProfileView.as_view()),
    path('<int:pk>/', views.UserProfileView.as_view()),
    path('deposit/<int:amount>/', views.deposit, name='deposit'),
    path('buy/', views.buy),
    path('reset/', views.reset),
]
